from django import template

register = template.Library()


@register.filter
def get_cell_status(status_map, args):
    try:
        user_id, optreden_id = args.split(':')
        return status_map.get((int(user_id), int(optreden_id)), '')
    except Exception:
        return ''


@register.simple_tag
def cell_key(user_id, optreden_id):
    return f'{user_id}:{optreden_id}'
