from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MemberProfile

User = get_user_model()


@receiver(post_save, sender=User)
def ensure_member_profile(sender, instance, created, **kwargs):
    profile, was_created = MemberProfile.objects.get_or_create(
        user=instance,
        defaults={
            'first_name': getattr(instance, 'first_name', '') or '',
            'last_name': getattr(instance, 'last_name', '') or '',
        },
    )

    if created and not was_created:
        profile.first_name = getattr(instance, 'first_name', '') or ''
        profile.last_name = getattr(instance, 'last_name', '') or ''
        profile.save(update_fields=['first_name', 'last_name'])
