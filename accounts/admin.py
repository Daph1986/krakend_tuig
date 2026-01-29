from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import MemberProfile


class MemberProfileInline(admin.StackedInline):
    model = MemberProfile
    can_delete = False
    extra = 0
    verbose_name_plural = 'Lidgegevens'


class CustomUserAdmin(UserAdmin):
    inlines = (MemberProfileInline,)

    def get_inline_instances(self, request, obj=None):
        # Inline pas tonen na opslaan van User
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
