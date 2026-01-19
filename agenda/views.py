from django.shortcuts import render
from .models import Optreden


def agenda(request):
    optredens = Optreden.objects.filter(openbaar=True)
    return render(request, 'agenda.html', {
        'optredens': optredens
    })
