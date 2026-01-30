from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import HttpResponse

from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm

from .forms import ProfileEditCombinedForm
from .models import MemberProfile


@login_required
def profile_detail(request):
    profile, _ = MemberProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile_detail.html', {'profile': profile})


@login_required
def profile_edit(request):
    profile, _ = MemberProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileEditCombinedForm(
            request.POST,
            user=request.user,
            profile_instance=profile,
            files=request.FILES,
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Je profiel is opgeslagen.')
            return redirect('accounts:profile_detail')
    else:
        form = ProfileEditCombinedForm(
            user=request.user,
            profile_instance=profile,
        )

    return render(request, 'profile_edit.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def members_list(request):
    base_qs = (
        MemberProfile.objects
        .filter(is_active=True)
        .exclude(user__username='HelloDaphneAdmin')
        .order_by('user__last_name', 'last_name_prefix', 'user__first_name')
    )

    muzikanten = base_qs.filter(role__icontains='muzikant')
    zangers = base_qs.exclude(role__icontains='muzikant')

    return render(request, 'members_list.html', {
        'zangers': zangers,
        'muzikanten': muzikanten,
    })


@login_required
def members_pdf(request):
    base_qs = (
        MemberProfile.objects
        .filter(is_active=True)
        .exclude(user__username='HelloDaphneAdmin')
        .order_by('user__last_name', 'last_name_prefix', 'user__first_name')
    )

    zangers = base_qs.exclude(role__icontains='muzikant')
    muzikanten = base_qs.filter(role__icontains='muzikant')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ledenlijst.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        leftMargin=10 * mm,
        rightMargin=10 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
    )

    styles = getSampleStyleSheet()

    cell_style = ParagraphStyle(
        'cell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=9,
    )
    header_style = ParagraphStyle(
        'header',
        parent=cell_style,
        fontName='Helvetica-Bold',
    )

    def p(text, style=cell_style):
        return Paragraph((text or '').replace('\n', '<br/>'), style)

    def make_table(qs):
        data = [[
            p('Achternaam', header_style),
            p('Voornaam', header_style),
            p('Adres', header_style),
            p('Postcode', header_style),
            p('Plaats', header_style),
            p('Telefoon', header_style),
            p('Email', header_style),
        ]]

        for m in qs:
            phone = (m.phone or '').replace(' / ', '\n').replace('/', '\n')
            data.append([
                p(m.sortable_last_name),
                p(m.user.first_name),
                p(m.address),
                p(m.postal_code),
                p(m.city),
                p(phone),
                p(m.user.email),
            ])

        ratios = [1.2, 1.0, 2.2, 0.8, 1.1, 1.1, 1.6]
        total = sum(ratios)
        col_widths = [doc.width * (r / total) for r in ratios]

        table = Table(data, repeatRows=1, colWidths=col_widths, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E6E6E6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7F7F7')]),
        ]))
        return table

    elements = [
        Paragraph('Ledenlijst', styles['Title']),
        Spacer(1, 8),

        Paragraph('Zangers', styles['Heading2']),
        Spacer(1, 4),
        make_table(zangers),

        Spacer(1, 12),

        Paragraph('Muzikanten', styles['Heading2']),
        Spacer(1, 4),
        make_table(muzikanten),
    ]

    doc.build(elements)
    return response


def logout_view(request):
    logout(request)
    messages.success(request, 'Je bent nu uitgelogd.')

    next_url = request.POST.get('next') or request.GET.get('next')

    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)

    return redirect('home')
