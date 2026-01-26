from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from sponsors.models import Sponsor
from django.db.models.functions import Lower

from .models import HomePageContent, HomeSlide, ZingMeeContent
from .forms import HomePageContentForm, HomeSlideForm, ZingMeeContentForm


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


@staff_member_required
def home_slides_list(request):
    homepage, _ = HomePageContent.objects.get_or_create(id=1)
    slides = homepage.slides.all()  # ook inactief, zodat je kunt beheren
    return render(request, 'slides_list.html', {'homepage': homepage, 'slides': slides})


@staff_member_required
def home_slide_create(request):
    homepage, _ = HomePageContent.objects.get_or_create(id=1)

    if request.method == 'POST':
        form = HomeSlideForm(request.POST, request.FILES)
        if form.is_valid():
            slide = form.save(commit=False)
            slide.homepage = homepage
            slide.save()
            messages.success(request, 'Slide toegevoegd.')
            return redirect('home_slides_list')
        messages.error(request, 'Controleer het formulier.')
    else:
        form = HomeSlideForm()

    return render(request, 'slide_form.html', {'form': form, 'mode': 'create'})


@staff_member_required
def home_slide_update(request, pk):
    homepage, _ = HomePageContent.objects.get_or_create(id=1)
    slide = get_object_or_404(HomeSlide, pk=pk, homepage=homepage)

    if request.method == 'POST':
        form = HomeSlideForm(request.POST, request.FILES, instance=slide)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slide opgeslagen.')
            return redirect('home_slides_list')
        messages.error(request, 'Controleer het formulier.')
    else:
        form = HomeSlideForm(instance=slide)

    return render(request, 'slide_form.html', {'form': form, 'mode': 'edit', 'slide': slide})


@staff_member_required
def home_slide_delete(request, pk):
    homepage, _ = HomePageContent.objects.get_or_create(id=1)
    slide = get_object_or_404(HomeSlide, pk=pk, homepage=homepage)

    if request.method == 'POST':
        slide.delete()
        messages.success(request, 'Slide verwijderd.')
        return redirect('home_slides_list')

    return render(request, 'slide_confirm_delete.html', {'slide': slide})


def zing_mee(request):
    content, _ = ZingMeeContent.objects.get_or_create(pk=1)
    return render(request, 'zing_mee.html', {'content': content})


@staff_member_required
def zing_mee_edit(request):
    content, _ = ZingMeeContent.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = ZingMeeContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'De pagina "Zing mee" is bijgewerkt.')
            return redirect('zing_mee')
    else:
        form = ZingMeeContentForm(instance=content)

    return render(request, 'zing_mee_edit.html', {'form': form})
