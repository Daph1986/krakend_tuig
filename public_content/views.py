from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import MemberProfile
from .forms import PhotoAlbumForm, AlbumPhotoForm, VideoForm
from .models import PhotoAlbum, AlbumPhoto, Video
from .permissions import can_manage_media


def media_overview(request):
    albums_all = PhotoAlbum.objects.filter(
        is_published=True
    ).prefetch_related('photos')

    albums = albums_all[:5]
    albums_total = albums_all.count()

    videos_all = Video.objects.filter(is_published=True)
    videos = videos_all[:5]
    videos_total = videos_all.count()

    members_all = MemberProfile.objects.filter(
        is_active=True,
        consent_public_profile=True,
    )
    members = members_all[:12]
    members_total = members_all.count()

    return render(
        request,
        'overview.html',
        {
            'albums': albums,
            'albums_total': albums_total,
            'videos': videos,
            'videos_total': videos_total,
            'members': members,
            'members_total': members_total,
        },
    )


def albums_list(request):
    albums = PhotoAlbum.objects.filter(
        is_published=True
    ).prefetch_related('photos')
    return render(
        request,
        'albums_list.html',
        {'albums': albums},
    )


def album_detail(request, slug):
    album = get_object_or_404(
        PhotoAlbum.objects.filter(is_published=True).prefetch_related('photos'),
        slug=slug,
    )
    return render(request, 'album_detail.html', {'album': album})


def videos_list(request):
    videos = Video.objects.filter(is_published=True)
    return render(request, 'videos_list.html', {'videos': videos})


def smoelenboek_public(request):
    members = MemberProfile.objects.filter(
        is_active=True,
        consent_public_profile=True,
    )
    return render(
        request,
        'smoelenboek_public.html',
        {'members': members},
    )


@login_required
def smoelenboek_private(request):
    members = MemberProfile.objects.filter(is_active=True)
    return render(
        request,
        'smoelenboek_private.html',
        {'members': members},
    )


manage_required = [
    login_required,
    user_passes_test(can_manage_media),
]


def _apply(decorators):
    def _decorator(view_func):
        for d in reversed(decorators):
            view_func = d(view_func)
        return view_func
    return _decorator


@_apply(manage_required)
def media_manage_home(request):
    return render(request, 'media_manage/home.html')


@_apply(manage_required)
def album_manage_list(request):
    albums = PhotoAlbum.objects.all().prefetch_related('photos')
    return render(request, 'media_manage/album_list.html', {'albums': albums})


@_apply(manage_required)
def album_create(request):
    if request.method == 'POST':
        form = PhotoAlbumForm(request.POST)
        if form.is_valid():
            album = form.save()
            messages.success(request, 'Album aangemaakt.')
            return redirect('public_content:album_update', pk=album.pk)
    else:
        form = PhotoAlbumForm()
    return render(request, 'media_manage/album_form.html', {'form': form, 'mode': 'create'})


@_apply(manage_required)
def album_update(request, pk):
    album = get_object_or_404(PhotoAlbum, pk=pk)
    photos = album.photos.all()

    if request.method == 'POST':
        form = PhotoAlbumForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, 'Album opgeslagen.')
            return redirect('public_content:album_update', pk=album.pk)
    else:
        form = PhotoAlbumForm(instance=album)

    return render(
        request,
        'media_manage/album_form.html',
        {'form': form, 'album': album, 'photos': photos, 'mode': 'update'},
    )


@_apply(manage_required)
def album_delete(request, pk):
    album = get_object_or_404(PhotoAlbum, pk=pk)
    if request.method == 'POST':
        album.delete()
        messages.success(request, 'Album verwijderd.')
        return redirect('public_content:album_manage_list')
    return render(request, 'media_manage/confirm_delete.html', {
        'title': 'Album verwijderen',
        'object_name': album.title,
        'cancel_url': redirect('public_content:album_manage_list').url,
    })


@_apply(manage_required)
def albumphoto_create(request, album_id):
    album = get_object_or_404(PhotoAlbum, pk=album_id)

    if request.method == 'POST':
        form = AlbumPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.album = album
            photo.save()
            messages.success(request, 'Foto toegevoegd.')
            return redirect('public_content:album_update', pk=album.pk)
    else:
        form = AlbumPhotoForm()

    return render(request, 'media_manage/photo_form.html', {'form': form, 'album': album, 'mode': 'create'})


@_apply(manage_required)
def albumphoto_update(request, pk):
    photo = get_object_or_404(AlbumPhoto, pk=pk)
    album = photo.album

    if request.method == 'POST':
        form = AlbumPhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Foto opgeslagen.')
            return redirect('public_content:album_update', pk=album.pk)
    else:
        form = AlbumPhotoForm(instance=photo)

    return render(
        request,
        'media_manage/photo_form.html',
        {
            'form': form,
            'album': album,
            'photo': photo,
            'mode': 'update',
        },
    )


@_apply(manage_required)
def albumphoto_delete(request, pk):
    photo = get_object_or_404(AlbumPhoto, pk=pk)
    album = photo.album
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Foto verwijderd.')
        return redirect('public_content:album_update', pk=album.pk)

    return render(request, 'media_manage/confirm_delete.html', {
        'title': 'Foto verwijderen',
        'object_name': photo.caption or photo.image.name,
        'cancel_url': redirect('public_content:album_update', pk=album.pk).url,
    })


@_apply(manage_required)
def video_manage_list(request):
    videos = Video.objects.all()
    return render(request, 'media_manage/video_list.html', {'videos': videos})


@_apply(manage_required)
def video_create(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video aangemaakt.')
            return redirect('public_content:video_manage_list')
    else:
        form = VideoForm()
    return render(request, 'media_manage/video_form.html', {'form': form, 'mode': 'create'})


@_apply(manage_required)
def video_update(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video opgeslagen.')
            return redirect('public_content:video_manage_list')
    else:
        form = VideoForm(instance=video)
    return render(request, 'media_manage/video_form.html', {'form': form, 'video': video, 'mode': 'update'})


@_apply(manage_required)
def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video verwijderd.')
        return redirect('public_content:video_manage_list')
    return render(request, 'media_manage/confirm_delete.html', {
        'title': 'Video verwijderen',
        'object_name': video.title,
        'cancel_url': redirect('public_content:video_manage_list').url,
    })
