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


class ZingMeeContent(models.Model):
    # Video
    video_url = models.URLField(
        default='https://www.youtube.com/embed/l6UBUZQzRHQ'
    )
    video_caption = models.CharField(
        max_length=200,
        default='Impressie van een oefenavond uit 2023'
    )

    # Praktische info
    repetities_regel_1 = models.CharField(max_length=100, default='Iedere maandagavond')
    repetities_regel_2 = models.CharField(max_length=100, default='19:30 – 21:30')
    repetities_toelichting = models.CharField(
        max_length=150,
        default='(behalve de eerste maandag van de maand)',
        blank=True
    )

    locatie_regel_1 = models.CharField(max_length=100, default='Parochiehuis')
    locatie_regel_2 = models.CharField(max_length=100, default='Herenstraat 15')
    locatie_regel_3 = models.CharField(max_length=100, default='3621 AP Breukelen')

    contact_kop = models.CharField(max_length=50, default='Interesse?')
    contact_naam = models.CharField(max_length=100, default='Gert Frankhuisen')
    contact_telefoon = models.CharField(max_length=20, default='0625011812')

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Zing mee – content'
