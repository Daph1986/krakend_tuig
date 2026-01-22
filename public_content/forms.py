from django import forms
from .models import PhotoAlbum, AlbumPhoto, Video


class PhotoAlbumForm(forms.ModelForm):
    class Meta:
        model = PhotoAlbum
        fields = ['title', 'date', 'description', 'order', 'is_published']
        labels = {
            'title': 'Titel',
            'date': 'Datum',
            'description': 'Beschrijving',
            'order': 'Volgorde',
            'is_published': 'Openbaar',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            else:
                widget.attrs['class'] = 'form-control'

        self.fields['date'].widget = forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            },
            format='%Y-%m-%d',
        )
        self.fields['date'].input_formats = ['%Y-%m-%d']


class AlbumPhotoForm(forms.ModelForm):
    class Meta:
        model = AlbumPhoto
        fields = ['image', 'caption', 'credit', 'order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'

            elif isinstance(widget, forms.FileInput):
                widget.attrs['class'] = 'form-control'

            else:
                widget.attrs['class'] = 'form-control'


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'date', 'description', 'url', 'file', 'is_embed', 'order', 'is_published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            else:
                widget.attrs['class'] = 'form-control'

        self.fields['date'].widget = forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
            },
            format='%Y-%m-%d',
        )
        self.fields['date'].input_formats = ['%Y-%m-%d']
