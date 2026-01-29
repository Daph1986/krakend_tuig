from django.shortcuts import render
from planning.models import Optreden


def agenda(request):
    optredens = (
        Optreden.objects
        .filter(
            actief=True,
            openbaar=True,   # 👈 dit is de sleutel
        )
        .order_by('datum', 'tijd')
    )

    return render(request, 'agenda.html', {'optredens': optredens})
