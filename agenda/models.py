from django.db import models


class Optreden(models.Model):
    datum = models.DateField()
    titel = models.CharField(max_length=200)
    tijd = models.CharField(max_length=50, blank=True)
    locatie = models.CharField(max_length=200, blank=True)
    openbaar = models.BooleanField(default=True)

    class Meta:
        ordering = ['datum']

    def __str__(self):
        return f'{self.datum} – {self.titel}'

    @property
    def tijd_display(self):
        if self.tijd:
            return f'{self.tijd} uur'
        return ''
