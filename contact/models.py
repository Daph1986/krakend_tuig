from django.db import models


class ContactPageContent(models.Model):
    secretariaat_titel = models.CharField(
        max_length=200, default='Adres secretariaat')
    secretariaat_regel1 = models.CharField(
        max_length=200, blank=True, default='Shantykoor Krakend Tuig')
    secretariaat_regel2 = models.CharField(max_length=200, blank=True)
    secretariaat_regel3 = models.CharField(max_length=200, blank=True)
    secretariaat_email = models.EmailField(blank=True)

    boeken_titel = models.CharField(max_length=200, default='Optreden boeken')
    boeken_naam = models.CharField(max_length=200, blank=True)
    boeken_tel = models.CharField(
        max_length=50, blank=True, help_text='Bijv. 0625011812')
    boeken_email = models.EmailField(blank=True)

    site_titel = models.CharField(
        max_length=200, default='Vragen of opmerkingen over de site')
    site_naam = models.CharField(max_length=200, blank=True)
    site_rol = models.CharField(max_length=200, blank=True, default='Webbeheerder')
    site_url = models.URLField(blank=True)
    site_url_label = models.CharField(
        max_length=200, blank=True, default='Hello Daphne')
    site_logo = models.ImageField(upload_to='contact/', blank=True, null=True)
    site_email = models.EmailField(blank=True)


updated_at = models.DateTimeField(auto_now=True)


def __str__(self):
    return 'Contactpagina content'
