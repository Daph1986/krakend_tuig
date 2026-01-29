from django.contrib import admin
from .models import Optreden


@admin.register(Optreden)
class OptredenAdmin(admin.ModelAdmin):
    list_display = (
        'datum',
        'titel',
        'tijd_display',
        'locatie',
        'openbaar',
        'actief',
    )
    list_filter = ('openbaar', 'actief', 'datum')
    search_fields = ('titel', 'locatie', 'adres')
    ordering = ('datum', 'tijd')

    def tijd_display(self, obj):
        return obj.tijd_display

    tijd_display.short_description = 'Tijd'
