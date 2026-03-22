from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from collections import defaultdict
from .forms import OptredenForm
from .models import Aanwezigheid, Optreden
from accounts.utils import get_member_groups
from datetime import timedelta
from django.utils import timezone


def is_planning_beheer(user):
    return user.is_staff or user.is_superuser


@login_required
def planning_overzicht(request):
    toon_archief = request.GET.get('archief') == '1'

    vandaag = timezone.now().date()
    grens_datum = vandaag - timedelta(days=7)

    optredens_qs = Optreden.objects.filter(actief=True)

    if not toon_archief:
        optredens_qs = optredens_qs.filter(datum__gte=grens_datum)

    optredens = optredens_qs.order_by('datum', 'tijd', 'titel')

    groups = get_member_groups()
    zangers = groups['zangers']
    zwaaibaas = groups['zwaaibaas']
    muzikanten = groups['muzikanten']

    leden = list(zangers) + list(zwaaibaas) + list(muzikanten)

    aanwez = Aanwezigheid.objects.filter(
        optreden__in=optredens,
        user_id__in=[m.user_id for m in leden],
    ).values('user_id', 'optreden_id', 'status')

    status_map = {(a['user_id'], a['optreden_id']): a['status'] for a in aanwez}

    aanwezig_telling = defaultdict(lambda: {'aanwezig': 0, 'afwezig': 0, 'onzeker': 0})

    for (user_id, optreden_id), status in status_map.items():
        if status in ('aanwezig', 'afwezig', 'onzeker'):
            aanwezig_telling[optreden_id][status] += 1

    context = {
        'optredens': optredens,
        'leden': leden,
        'zangers': zangers,
        'zwaaibaas': zwaaibaas,
        'muzikanten': muzikanten,
        'status_map': status_map,
        'aanwezig_telling': dict(aanwezig_telling),
        'status_choices': Aanwezigheid.STATUS_CHOICES,
        'is_beheer': is_planning_beheer(request.user),
        'current_user_id': request.user.id,
        'toon_archief': toon_archief,
    }

    return render(request, 'planning.html', context)


@require_POST
@login_required
def planning_status_update(request):
    try:
        optreden_id = int(request.POST.get('optreden_id', ''))
    except ValueError:
        return HttpResponseBadRequest('Ongeldig optreden_id')

    status = request.POST.get('status', '')  # '' of 'aanwezig'/'afwezig'/'onzeker'
    allowed_statuses = {c[0] for c in Aanwezigheid.STATUS_CHOICES}

    if status != '' and status not in allowed_statuses:
        return HttpResponseBadRequest('Ongeldige status')

    target_user_id = request.user.id

    # alleen beheer mag voor anderen
    if is_planning_beheer(request.user) and request.POST.get('user_id'):
        try:
            target_user_id = int(request.POST.get('user_id'))
        except ValueError:
            return HttpResponseBadRequest('Ongeldig user_id')

    optreden = get_object_or_404(Optreden, pk=optreden_id)

    Aanwezigheid.objects.update_or_create(
        optreden=optreden,
        user_id=target_user_id,
        defaults={'status': (status or None)},
    )

    return JsonResponse({'ok': True})


@login_required
@user_passes_test(is_planning_beheer)
def optreden_create(request):
    if request.method == 'POST':
        form = OptredenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('planning:overzicht')
    else:
        form = OptredenForm()

    return render(request, 'planning_optreden_form.html', {'form': form, 'mode': 'create'})


@login_required
@user_passes_test(is_planning_beheer)
def optreden_update(request, pk):
    optreden = get_object_or_404(Optreden, pk=pk)

    if request.method == 'POST':
        form = OptredenForm(request.POST, instance=optreden)
        if form.is_valid():
            form.save()
            return redirect('planning:overzicht')
    else:
        form = OptredenForm(instance=optreden)

    return render(request, 'planning_optreden_form.html', {'form': form, 'mode': 'edit', 'optreden': optreden})


@login_required
@user_passes_test(is_planning_beheer)
def optreden_delete(request, pk):
    optreden = get_object_or_404(Optreden, pk=pk)

    if request.method == 'POST':
        optreden.delete()
        return redirect('planning:overzicht')

    return render(request, 'planning_optreden_confirm_delete.html', {'optreden': optreden})
