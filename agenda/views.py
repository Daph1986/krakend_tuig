from django.shortcuts import render
from planning.models import Optreden


def agenda(request):
    qs = Optreden.objects.filter(actief=True)

    if not request.user.is_authenticated or not request.user.has_perm('planning.change_optreden'):
        qs = qs.filter(openbaar=True)

    optredens = qs.order_by('datum', 'tijd')
    return render(request, 'agenda.html', {'optredens': optredens})
