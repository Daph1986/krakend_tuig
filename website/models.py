from django.db import models


class HomePageContent(models.Model):

    hero_image = models.ImageField(upload_to='home/', blank=True, null=True)

    welkom_titel = models.CharField(
        max_length=200, default='Welkom bij shantykoor Krakend Tuig')
    welkom_tekst = models.TextField(blank=True)

    mededelingen_titel = models.CharField(
        max_length=200, default='Mededelingen')
    mededelingen_tekst = models.TextField(blank=True)
    mededelingen_email = models.EmailField(
        blank=True,
        help_text='Wordt als klikbare e-mail weergegeven'
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Homepage content'


class HomeSlide(models.Model):
    homepage = models.ForeignKey(
        HomePageContent, on_delete=models.CASCADE, related_name='slides')
    image = models.ImageField(upload_to='home/slides/')
    caption = models.CharField(max_length=255, blank=True)
    credit = models.CharField(max_length=255, blank=True)
    interval_ms = models.PositiveIntegerField(default=5000)
    volgorde = models.PositiveIntegerField(default=0)
    actief = models.BooleanField(default=True)

    class Meta:
        ordering = ['volgorde', 'id']

    def __str__(self):
        return self.caption or f'Slide {self.id}'
