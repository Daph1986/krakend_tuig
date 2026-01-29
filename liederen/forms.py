from django import forms
from .models import Lied


class LiedForm(forms.ModelForm):
    class Meta:
        model = Lied
        fields = ['nummer', 'titel', 'pdf', 'actief', 'volgorde']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            else:
                widget.attrs['class'] = 'form-control'

        self.fields['pdf'].help_text = 'Upload een pdf-bestand.'
