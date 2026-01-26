from django.db import models


def about_upload_to(instance, filename):
    return f'about/{filename}'


class AboutIntro(models.Model):
    title = models.CharField(
        max_length=200,
        default='“Krakend Tuig” – shanty zoals het altijd was'
    )

    paragraph_1 = models.TextField(blank=True)
    paragraph_2 = models.TextField(blank=True)
    paragraph_3 = models.TextField(blank=True)
    paragraph_4 = models.TextField(blank=True)
    paragraph_5 = models.TextField(blank=True)
    paragraph_6 = models.TextField(blank=True)
    paragraph_7 = models.TextField(blank=True)

    image = models.ImageField(
        upload_to=about_upload_to,
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Leer ons kennen – intro'
