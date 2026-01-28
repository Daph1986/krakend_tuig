from django import template

register = template.Library()


@register.filter
def split_lines(value, sep='/'):
    if not value:
        return ''
    parts = [p.strip() for p in str(value).split(sep) if p.strip()]
    return '\n'.join(parts)
