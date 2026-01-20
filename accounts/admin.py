from django.contrib import admin
from .models import MemberProfile


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'role', 'consent_public_profile', 'is_active')
    list_filter = ('consent_public_profile', 'is_active')
    search_fields = ('first_name', 'last_name', 'role', 'user__username', 'user__email')
