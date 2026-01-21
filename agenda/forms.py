from django import forms
from .models import Optreden


class OptredenForm(forms.ModelForm):
    class Meta:
        model = Optreden
        fields = ['datum', 'titel', 'tijd', 'locatie', 'openbaar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            else:
                widget.attrs['class'] = 'form-control'

        self.fields['datum'].widget = forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            },
            format='%Y-%m-%d',
        )
        self.fields['datum'].input_formats = ['%Y-%m-%d']

        self.fields['tijd'].widget = forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control',
            },
            format='%H:%M',
        )
        self.fields['tijd'].input_formats = ['%H:%M']
