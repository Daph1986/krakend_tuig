from django import forms
from .models import AboutIntro


class AboutIntroForm(forms.ModelForm):
    class Meta:
        model = AboutIntro
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
