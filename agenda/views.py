from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Optreden
from .forms import OptredenForm


def agenda(request):
    qs = Optreden.objects.all()

    if not request.user.is_authenticated or not request.user.has_perm('agenda.change_optreden'):
        qs = qs.filter(openbaar=True)

    optredens = qs.order_by('datum')
    return render(request, 'agenda.html', {'optredens': optredens})


@login_required
@permission_required('agenda.add_optreden', raise_exception=True)
def optreden_create(request):
    form = OptredenForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('agenda:overzicht')
    return render(request, 'optreden_form.html', {'form': form})


@login_required
@permission_required('agenda.change_optreden', raise_exception=True)
def optreden_update(request, pk):
    optreden = get_object_or_404(Optreden, pk=pk)
    form = OptredenForm(request.POST or None, instance=optreden)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('agenda:overzicht')
    return render(request, 'optreden_form.html', {'form': form, 'optreden': optreden})


@login_required
@permission_required('agenda.delete_optreden', raise_exception=True)
def optreden_delete(request, pk):
    optreden = get_object_or_404(Optreden, pk=pk)
    if request.method == 'POST':
        optreden.delete()
        return redirect('agenda:overzicht')
    return render(request, 'optreden_confirm_delete.html', {'optreden': optreden})
