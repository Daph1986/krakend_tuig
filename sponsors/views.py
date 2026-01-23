from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.functions import Lower
from .models import Sponsor
from .forms import SponsorForm


def is_staff(user):
    return user.is_staff


def sponsoren(request):
    sponsors = Sponsor.objects.filter(actief=True).order_by('volgorde', Lower('naam'))
    return render(request, 'sponsors_vrienden_sponsors.html', {'sponsors': sponsors})


@login_required
@user_passes_test(is_staff)
def sponsor_beheer(request):
    sponsors = Sponsor.objects.all().order_by('volgorde', Lower('naam'))
    return render(request, 'sponsors_beheer.html', {'sponsors': sponsors})


@login_required
@user_passes_test(is_staff)
def sponsor_toevoegen(request):
    form = SponsorForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('sponsors:beheer')
    return render(request, 'sponsors_form.html', {'form': form, 'titel': 'Sponsor toevoegen'})


@login_required
@user_passes_test(is_staff)
def sponsor_bewerken(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    form = SponsorForm(request.POST or None, request.FILES or None, instance=sponsor)
    if form.is_valid():
        form.save()
        return redirect('sponsors:beheer')
    return render(request, 'sponsors_form.html', {'form': form, 'titel': 'Sponsor bewerken'})


@login_required
@user_passes_test(is_staff)
def sponsor_verwijderen(request, pk):
    sponsor = get_object_or_404(Sponsor, pk=pk)
    if request.method == 'POST':
        sponsor.delete()
        return redirect('sponsors:beheer')
    return render(request, 'sponsors_verwijderen.html', {'sponsor': sponsor})
