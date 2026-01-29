from django.db import models


class Lied(models.Model):
    nummer = models.PositiveIntegerField()
    titel = models.CharField(max_length=200)
    pdf = models.FileField(upload_to='liedteksten/')
    actief = models.BooleanField(default=True)
    volgorde = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['volgorde', 'nummer']

    def __str__(self):
        return f'{self.nummer}. {self.titel}'
