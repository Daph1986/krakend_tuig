from django.contrib import admin
from .models import Optreden


@admin.register(Optreden)
class OptredenAdmin(admin.ModelAdmin):
    list_display = ('datum', 'titel', 'tijd', 'locatie', 'openbaar')
    list_filter = ('openbaar', 'datum')
    search_fields = ('titel', 'locatie')
    ordering = ('datum',)
