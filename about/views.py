from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import AboutIntro
from .forms import AboutIntroForm


def about_page(request):
    intro, _ = AboutIntro.objects.get_or_create(pk=1)
    return render(request, 'about.html', {'intro': intro})


@staff_member_required
def about_intro_edit(request):
    intro, _ = AboutIntro.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = AboutIntroForm(request.POST, request.FILES, instance=intro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Intro van "Leer ons kennen" is bijgewerkt.')
            return redirect('about:about_page')
    else:
        form = AboutIntroForm(instance=intro)

    return render(request, 'about_intro_edit.html', {'form': form})
