from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')

    first_name = models.CharField(max_length=80)
    last_name = models.CharField('Achternaam', max_length=80)
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
    email = models.EmailField('Email', blank=True)

    consent_public_profile = models.BooleanField(
        default=False,
        help_text='Toon mij in het openbare smoelenboek',
    )

    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'last_name_prefix', 'first_name']

    @property
    def full_last_name(self):
        if self.last_name_prefix:
            return f'{self.last_name_prefix} {self.last_name}'
        return self.last_name

    @property
    def sortable_last_name(self):
        if self.last_name_prefix:
            return f'{self.last_name}, {self.last_name_prefix}'
        return self.last_name

    def __str__(self):
        return f'{self.first_name} {self.full_last_name}'.strip() or self.user.get_username()
