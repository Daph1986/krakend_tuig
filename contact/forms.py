from django import forms
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    """
    Form for the contact page
    """
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=150, required=True)
    phone_number = forms.CharField(max_length=12, required=False)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(
        max_length=2500, widget=forms.Textarea, required=True)
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        """
        Contact form which is displayed at
        contact page with placeholders
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': _('Voornaam'),
            'last_name': _('Achternaam'),
            'email': _('Email adres'),
            'phone_number': _('Telefoonnummer'),
            'subject': _('Onderwerp'),
            'message': _('Waar kunnen we je mee helpen? Typ hier je bericht...'),
        }

        self.fields['message'].widget.attrs = {'rows': 8}
        self.fields['first_name'].widget.attrs['autofocus'] = True

        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs['placeholder'] = f"{placeholder} *"
            self.fields[field_name].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field_name].label = False
