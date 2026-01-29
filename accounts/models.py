from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')

    last_name_prefix = models.CharField(
        'Tussenvoegsel',
        max_length=30,
        blank=True,
        help_text='Bijv. van, van der, de, ten',
    )

    role = models.CharField(max_length=120, blank=True)
    photo = models.ImageField(upload_to='members/', blank=True)

    address = models.CharField('Adres', max_length=200, blank=True)
    postal_code = models.CharField('Postcode', max_length=20, blank=True)
    city = models.CharField('Plaats', max_length=120, blank=True)
    phone = models.CharField('Telefoon', max_length=50, blank=True)

    consent_public_profile = models.BooleanField(
        default=False,
        help_text='Toon mij in het openbare smoelenboek',
    )

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name', 'last_name_prefix']

    @property
    def full_last_name(self):
        ln = (self.user.last_name or '').strip()
        prefix = (self.last_name_prefix or '').strip()

        if prefix:
            return f'{prefix} {ln}'.strip()
        return ln

    @property
    def sortable_last_name(self):
        ln = (self.user.last_name or '').strip()
        if self.last_name_prefix:
            return f'{ln}, {self.last_name_prefix}'.strip(', ')
        return ln

    def __str__(self):
        fn = (self.user.first_name or '').strip()
        return f'{fn} {self.full_last_name}'.strip() or self.user.get_username()

    @property
    def display_name(self):
        fn = (self.user.first_name or '').strip()
        return f'{fn} {self.full_last_name}'.strip() or self.user.get_username()

    @property
    def display_name_lastname_comma(self):
        """
        Miltenburg, van Lydia
        Agterberg Kees (zonder komma als er geen prefix is)
        """
        last = (self.user.last_name or '').strip()
        prefix = (self.last_name_prefix or '').strip()
        first = (self.user.first_name or '').strip()

        if prefix:
            return f'{last}, {prefix} {first}'.strip()
        return f'{last} {first}'.strip()
