from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import AboutIntro
from .forms import AboutIntroForm
from accounts.models import MemberProfile


def about_page(request):
    intro, _ = AboutIntro.objects.get_or_create(pk=1)
    active_members = MemberProfile.objects.filter(is_active=True, user__is_active=True)

    # Tel exact op basis van de rollen 'muzikant' en 'zanger'
    muzikanten_count = active_members.filter(role__iexact='muzikant').count()
    zangers_count = active_members.filter(role__iexact='zanger').count()

    # Vervang {muzikanten} en {zangers} veilig in de teksten
    def format_paragraph(text):
        if not text:
            return text
        return text.replace('{muzikanten}', str(muzikanten_count)).replace('{zangers}', str(zangers_count))

    processed_paragraphs = {
        'paragraph_1': format_paragraph(intro.paragraph_1),
        'paragraph_2': format_paragraph(intro.paragraph_2),
        'paragraph_3': format_paragraph(intro.paragraph_3),
        'paragraph_4': format_paragraph(intro.paragraph_4),
        'paragraph_5': format_paragraph(intro.paragraph_5),
        'paragraph_6': format_paragraph(intro.paragraph_6),
        'paragraph_7': format_paragraph(intro.paragraph_7),
    }

    context = {
        'intro': intro,
        'paragraphs': processed_paragraphs,
        'muzikanten_count': muzikanten_count,
        'zangers_count': zangers_count,
    }

    return render(request, 'about.html', context)


@staff_member_required
def about_intro_edit(request):
    intro, _ = AboutIntro.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = AboutIntroForm(request.POST, request.FILES, instance=intro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Intro van "Leer ons kennen" is bijgewerkt.')
            return redirect('about:about_page')
    else:
        form = AboutIntroForm(instance=intro)

    return render(request, 'about_intro_edit.html', {'form': form})
