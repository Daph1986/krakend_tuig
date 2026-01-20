from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from accounts.models import MemberProfile
from .models import PhotoAlbum, Video


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
