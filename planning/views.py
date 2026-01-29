from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import MemberProfile
from .forms import OptredenForm
from .models import Aanwezigheid, Optreden


def is_planning_beheer(user):
    return user.is_staff or user.is_superuser


@login_required
def planning_overzicht(request):
    optredens = Optreden.objects.filter(actief=True).order_by('datum', 'tijd', 'titel')

    leden = (
        MemberProfile.objects
        .filter(is_active=True)
        .exclude(user__username='HelloDaphneAdmin')
        .select_related('user')
        .order_by('last_name', 'last_name_prefix', 'first_name')
    )

    aanwez = Aanwezigheid.objects.filter(
        optreden__in=optredens,
        user__in=[m.user_id for m in leden],
    ).values('user_id', 'optreden_id', 'status')

    status_map = {(a['user_id'], a['optreden_id']): a['status'] for a in aanwez}

    context = {
        'optredens': optredens,
        'leden': leden,
        'status_map': status_map,
        'status_choices': Aanwezigheid.STATUS_CHOICES,
        'is_beheer': is_planning_beheer(request.user),
        'current_user_id': request.user.id,
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
