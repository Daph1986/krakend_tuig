from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    role = models.CharField(max_length=120, blank=True)
    photo = models.ImageField(upload_to='members/', blank=True)

    consent_public_profile = models.BooleanField(
        default=False,
        help_text='Toon mij in het openbare smoelenboek',
    )

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.user.get_username()
