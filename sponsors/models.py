from django.db import models


class Sponsor(models.Model):
    naam = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='sponsors/')
    volgorde = models.PositiveIntegerField(default=0)
    actief = models.BooleanField(default=True)

    class Meta:
        ordering = ['volgorde', 'naam']

    def __str__(self):
        return self.naam
