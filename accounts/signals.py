from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MemberProfile

User = get_user_model()


@receiver(post_save, sender=User)
def ensure_member_profile(sender, instance, created, **kwargs):
    if created:
        MemberProfile.objects.create(
            user=instance,
            first_name=getattr(instance, 'first_name', '') or '',
            last_name=getattr(instance, 'last_name', '') or '',
            email=getattr(instance, 'email', '') or '',
        )
