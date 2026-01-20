from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from accounts.models import MemberProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Create missing MemberProfile rows for existing users.'

    def handle(self, *args, **options):
        created_count = 0

        for user in User.objects.all():
            _, created = MemberProfile.objects.get_or_create(
                user=user,
                defaults={
                    'first_name': getattr(user, 'first_name', '') or '',
                    'last_name': getattr(user, 'last_name', '') or '',
                },
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Created {created_count} missing profiles.')
        )
