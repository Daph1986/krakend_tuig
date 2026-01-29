from django.conf import settings
from django.db import models


class Optreden(models.Model):
    titel = models.CharField(max_length=200)
    datum = models.DateField()
    tijd = models.TimeField(blank=True, null=True)
    locatie = models.CharField(max_length=255, blank=True)
    adres = models.TextField(blank=True)

    actief = models.BooleanField(default=True)
    openbaar = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.titel} ({self.datum})'

    @property
    def tijd_display(self):
        if self.tijd:
            return f'{self.tijd.strftime("%H:%M")} uur'
        return ''


class Aanwezigheid(models.Model):
    AANWEZIG = 'aanwezig'
    AFWEZIG = 'afwezig'
    ONZEKER = 'onzeker'

    STATUS_CHOICES = [
        (AANWEZIG, 'Aanwezig'),
        (AFWEZIG, 'Afwezig'),
        (ONZEKER, 'Nog niet zeker'),
    ]

    optreden = models.ForeignKey(Optreden, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # ✅ default weg, mag leeg zijn
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        blank=True,
        null=True,
    )

    bijgewerkt_op = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['optreden', 'user'], name='unique_aanwezigheid_per_optreden_per_user')
        ]
