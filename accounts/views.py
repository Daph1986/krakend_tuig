from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import MemberProfileForm
from .models import MemberProfile


@login_required
def profile_detail(request):
    profile, _ = MemberProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile_detail.html', {'profile': profile})


@login_required
def profile_edit(request):
    profile, _ = MemberProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = MemberProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Je profiel is opgeslagen.')
            return redirect('accounts:profile_detail')
    else:
        form = MemberProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {
        'form': form,
        'profile': profile,
    })


def logout_view(request):
    logout(request)
    messages.success(request, 'Je bent nu uitgelogd.')

    next_url = request.POST.get('next') or request.GET.get('next')

    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)

    return redirect('home')
