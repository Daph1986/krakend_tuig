from django.shortcuts import render
from planning.models import Optreden
from django.utils import timezone


def agenda(request):
    vandaag = timezone.now().date()

    optredens = (
        Optreden.objects
        .filter(
            actief=True,
            openbaar=True,
            datum__gte=vandaag
        )
        .order_by('datum', 'tijd')
    )

    return render(request, 'agenda.html', {'optredens': optredens})
