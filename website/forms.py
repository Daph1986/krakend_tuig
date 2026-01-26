from django import forms
from .models import HomePageContent


class HomePageContentForm(forms.ModelForm):
    class Meta:
        model = HomePageContent
        fields = [
            'hero_image',
            'welkom_titel',
            'welkom_tekst',
            'mededelingen_tekst',
            'mededelingen_email',
        ]

        widgets = {
            'welkom_tekst': forms.Textarea(attrs={'rows': 5}),
            'mededelingen_tekst': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.ClearableFileInput):
                widget.attrs['class'] = 'form-control'
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, forms.Textarea):
                widget.attrs['class'] = 'form-control'
            else:
                widget.attrs['class'] = 'form-control'
