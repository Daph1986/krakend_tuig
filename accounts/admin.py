from django.contrib import admin
from .models import MemberProfile


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'last_name_prefix',
        'role',
        'city',
        'phone',
        'email',
        'consent_public_profile',
        'is_active',
    )
    list_filter = ('consent_public_profile', 'is_active', 'city')
    search_fields = ('first_name', 'last_name', 'role',
                     'email', 'user__username', 'user__email')
