from django import forms
from .models import MemberProfile


class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['first_name', 'last_name', 'role', 'photo', 'consent_public_profile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, forms.ClearableFileInput):
                widget.attrs['class'] = 'form-control'
            else:
                widget.attrs['class'] = 'form-control'
