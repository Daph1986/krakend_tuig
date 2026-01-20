from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from accounts.models import MemberProfile
from .models import PhotoAlbum, Video


def media_overview(request):
    albums = PhotoAlbum.objects.filter(
        is_published=True
    ).prefetch_related('photos')

    videos = Video.objects.filter(is_published=True)

    members = MemberProfile.objects.filter(
        is_active=True,
        consent_public_profile=True,
    )

    return render(
        request,
        'overview.html',
        {
            'albums': albums,
            'videos': videos,
            'members': members,
        },
    )


def album_detail(request, slug):
    album = get_object_or_404(
        PhotoAlbum.objects.filter(is_published=True).prefetch_related('photos'),
        slug=slug,
    )
    return render(
        request,
        'album_detail.html',
        {'album': album},
    )


# Deze mag blijven bestaan (bijv. voor directe URL of later gebruik)
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
