from django import forms
from .models import HomePageContent
from .models import HomeSlide
from .models import ZingMeeContent


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


class HomeSlideForm(forms.ModelForm):
    class Meta:
        model = HomeSlide
        fields = ['image', 'caption', 'credit', 'interval_ms', 'volgorde', 'actief']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 2}),
            'credit': forms.Textarea(attrs={'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            else:
                widget.attrs['class'] = 'form-control'


class ZingMeeContentForm(forms.ModelForm):
    class Meta:
        model = ZingMeeContent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
