from django import forms
from .models import MemberProfile


class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['first_name', 'last_name', 'role', 'photo', 'consent_public_profile']
