from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages
from sponsors.models import Sponsor
from django.db.models.functions import Lower

from .models import HomePageContent
from .forms import HomePageContentForm


def home(request):
    homepage, _ = HomePageContent.objects.get_or_create(id=1)

    sponsors = Sponsor.objects.filter(actief=True).order_by('volgorde', Lower('naam'))
    slides = homepage.slides.filter(actief=True)

    context = {
        'homepage': homepage,
        'sponsors': sponsors,
        'slides': slides,
    }
    return render(request, 'index.html', context)


@staff_member_required
def homepage_edit(request):
    homepage, _ = HomePageContent.objects.get_or_create(id=1)

    if request.method == 'POST':
        form = HomePageContentForm(request.POST, request.FILES, instance=homepage)
        if form.is_valid():
            form.save()
            messages.success(request, 'Homepage opgeslagen.')
            return redirect('home')
        messages.error(request, 'Controleer het formulier.')
    else:
        form = HomePageContentForm(instance=homepage)

    return render(request, 'homepage_edit.html', {'form': form})


def zing_mee(request):
    return render(request, 'zing_mee.html')
