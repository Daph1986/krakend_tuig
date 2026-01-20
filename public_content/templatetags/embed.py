from django import template
from urllib.parse import urlparse, parse_qs

register = template.Library()


@register.filter
def embed_url(url):
    if not url:
        return ''

    url = url.strip()
    u = urlparse(url)

    host = (u.hostname or '').lower()
    path = (u.path or '').strip('/')

    # Als het al een embed url is: gewoon teruggeven
    if 'youtube.com' in host and path.startswith('embed/'):
        return url

    # YouTube watch?v=
    if 'youtube.com' in host:
        q = parse_qs(u.query)
        vid = (q.get('v') or [''])[0]
        if vid:
            return f'https://www.youtube.com/embed/{vid}'

        # shorts/VIDEOID
        if path.startswith('shorts/'):
            vid = path.split('/', 1)[1]
            if vid:
                return f'https://www.youtube.com/embed/{vid}'

        # live/VIDEOID
        if path.startswith('live/'):
            vid = path.split('/', 1)[1]
            if vid:
                return f'https://www.youtube.com/embed/{vid}'

    # youtu.be/VIDEOID
    if 'youtu.be' in host:
        vid = path.split('/')[0]
        if vid:
            return f'https://www.youtube.com/embed/{vid}'

    # Vimeo
    if 'vimeo.com' in host:
        vid = path.split('/')[-1]
        if vid.isdigit():
            return f'https://player.vimeo.com/video/{vid}'

    return url
