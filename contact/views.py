from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.mail import EmailMessage, BadHeaderError
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext as _

from .forms import ContactForm


def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        honeypot = request.POST.get('honeypot')

        if honeypot:
            return HttpResponseBadRequest(_("Spam detected"))

        if contact_form.is_valid():
            first_name = contact_form.cleaned_data['first_name']
            last_name = contact_form.cleaned_data['last_name']
            email = contact_form.cleaned_data['email']
            phone_number = contact_form.cleaned_data['phone_number']

            subject = contact_form.cleaned_data['subject']
            subject = " ".join(subject.splitlines()).strip()

            message = contact_form.cleaned_data['message']

            html_msg = render_to_string('contact_email.html', {
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'email': email,
                'subject': subject,
                'message': message
            })

            try:
                email_msg = EmailMessage(
                    subject=f"[Contact] {subject}",
                    body=html_msg,
                    from_email=f"Krakend Tuig <{settings.DEFAULT_FROM_EMAIL}>",
                    to=[settings.CONTACT_RECIPIENT_EMAIL],
                    headers={"Reply-To": email},
                )
                email_msg.content_subtype = "html"
                email_msg.send(fail_silently=False)

            except BadHeaderError:
                return HttpResponse(_('Invalid header found.'))
            except Exception:
                messages.error(request, _("Het bericht kon niet worden verzonden. Probeer het later opnieuw."))
                return render(request, 'contact.html', {'contact_form': contact_form})

            messages.success(request, _("Bedankt voor je bericht. We nemen spoedig contact met je op."))
            return redirect(reverse('home'))

    else:
        contact_form = ContactForm()

    return render(request, 'contact.html', {'contact_form': contact_form})
