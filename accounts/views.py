from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import MemberProfileForm


@login_required
def profile_edit(request):
    profile = request.user.member_profile

    if request.method == 'POST':
        form = MemberProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile_edit')
    else:
        form = MemberProfileForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {'form': form})
