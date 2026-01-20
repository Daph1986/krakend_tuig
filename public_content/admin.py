from django.contrib import admin
from .models import PhotoAlbum, AlbumPhoto, Video


class AlbumPhotoInline(admin.TabularInline):
    model = AlbumPhoto
    extra = 0
    fields = ('order', 'image', 'caption', 'credit')
    ordering = ('order',)


@admin.register(PhotoAlbum)
class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'order', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AlbumPhotoInline]
    ordering = ('order', '-date')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'order', 'is_published', 'is_embed')
    list_filter = ('is_published',)
    search_fields = ('title', 'description', 'url')
    ordering = ('order', '-date')

    fields = (
        'title',
        'date',
        'description',
        'url',
        'file',
        'is_embed',
        'order',
        'is_published',
    )
