from django import forms
from .models import Sponsor


class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ['naam', 'website', 'logo', 'volgorde', 'actief']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            else:
                widget.attrs['class'] = 'form-control'

        self.fields['website'].widget.attrs['placeholder'] = 'https://...'

        self.fields['logo'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/*',
        })
