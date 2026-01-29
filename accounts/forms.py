from django import forms
from django.contrib.auth import get_user_model

from .models import MemberProfile

User = get_user_model()


class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = [
            'role',
            'photo',
            'address',
            'postal_code',
            'city',
            'phone',
            'consent_public_profile',
        ]
        labels = {
            'role': 'Rol binnen het koor',
            'photo': 'Profielfoto',
            'address': 'Adres',
            'postal_code': 'Postcode',
            'city': 'Plaats',
            'phone': 'Telefoonnummer(s)',
            'consent_public_profile': 'Toon mij in het openbare smoelenboek',
        }
        help_texts = {
            'phone': 'Meerdere nummers? Gebruik een / (bijv. 030-1234567 / 06-12345678)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, forms.ClearableFileInput):
                widget.attrs.update({
                    'class': 'form-control',
                    'accept': 'image/*',
                })
            else:
                widget.attrs['class'] = 'form-control'


class ProfileEditCombinedForm(forms.Form):
    first_name = forms.CharField(label='Voornaam', required=False, disabled=True)
    last_name = forms.CharField(label='Achternaam', required=False, disabled=True)
    email = forms.EmailField(label='E-mailadres', required=False, disabled=True)

    def __init__(self, *args, user=None, profile_instance=None, files=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

        # subform voor MemberProfile
        self.profile_form = MemberProfileForm(
            data=(args[0] if args else None),
            files=files,
            instance=profile_instance,
        )

        # bootstrap styling voor user velden
        for name in ('first_name', 'last_name', 'email'):
            self.fields[name].widget.attrs['class'] = 'form-control'

    def is_valid(self):
        return super().is_valid() and self.profile_form.is_valid()

    def save(self):
        return self.profile_form.save()
