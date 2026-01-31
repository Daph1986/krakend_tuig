from django.core.management.base import BaseCommand
from accounts.models import MemberProfile


class Command(BaseCommand):
    help = 'Forceer wachtwoord wijzigen bij volgende login (behalve uitzonderingen)'

    def handle(self, *args, **options):
        exclude_usernames = ['HelloDaphneAdmin', 'gertfrankhuisen']

        qs = (
            MemberProfile.objects
            .filter(is_active=True)
            .exclude(user__username__in=exclude_usernames)
        )

        updated = qs.update(must_change_password=True)
        self.stdout.write(self.style.SUCCESS(
            f'{updated} leden gemarkeerd voor verplichte wachtwoordwijziging.'
        ))
