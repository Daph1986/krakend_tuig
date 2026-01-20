from django.db import models
from django.utils.text import slugify


class PhotoAlbum(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    date = models.DateField(null=True, blank=True, help_text='Bijv. datum optreden')
    description = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-date', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:120] or 'album'
            slug = base
            i = 2
            while PhotoAlbum.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{i}'
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class AlbumPhoto(models.Model):
    album = models.ForeignKey(PhotoAlbum, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='albums/%Y/%m/')
    caption = models.CharField(max_length=160, blank=True)
    credit = models.CharField(max_length=120, blank=True, help_text='Bijv. Foto: Naam')
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.album.title} - {self.caption or self.image.name}'


class Video(models.Model):
    title = models.CharField(max_length=140)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    url = models.URLField(
        blank=True,
        help_text='YouTube/Vimeo link (optioneel)',
    )

    file = models.FileField(
        upload_to='videos/%Y/%m/',
        blank=True,
        help_text='Upload een MP4-bestand (optioneel)',
    )

    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    is_embed = models.BooleanField(
        default=True,
        help_text='Vink uit als embed niet werkt; dan tonen we een linkknop',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-date', 'title']

    def __str__(self):
        return self.title
