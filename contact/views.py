from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings
from django.utils.translation import gettext as _


def contact(request):
    """
    View to return contact page and handle contact form submissions
    """
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        honeypot = request.POST.get('honeypot')

        if honeypot:
            # Honeypot field is filled out, likely spam
            return HttpResponseBadRequest(_("Spam detected"))

        if contact_form.is_valid():
            first_name = contact_form.cleaned_data['first_name']
            last_name = contact_form.cleaned_data['last_name']
            email = contact_form.cleaned_data['email']
            phone_number = contact_form.cleaned_data['phone_number']
            subject = contact_form.cleaned_data['subject']
            message = contact_form.cleaned_data['message']
            html_msg = render_to_string(
                'contact_email.html',
                {
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone_number': phone_number,
                    'email': email,
                    'subject': subject,
                    'message': message
                })
            try:
                send_mail(
                    subject, message, settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    html_message=html_msg, fail_silently=False
                )
            except BadHeaderError:
                return HttpResponse(_('Invalid header found.'))
            success_message = _(
                "Bedankt voor je bericht. "
                "We nemen spoedig contact met je op."
            )
            return redirect(reverse('home'), messages.success(
                request, success_message
            ))
    else:
        contact_form = ContactForm()

    template = 'contact.html'
    context = {
        'contact_form': contact_form,
    }

    return render(request, template, context)
