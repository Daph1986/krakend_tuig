from .models import MemberProfile

EXCLUDE_USERNAME_DEFAULT = 'HelloDaphneAdmin'


def get_member_groups(exclude_username: str = EXCLUDE_USERNAME_DEFAULT):
    base_qs = (
        MemberProfile.objects
        .filter(is_active=True)
        .exclude(user__username=exclude_username)
        .select_related('user')
        .order_by('user__last_name', 'last_name_prefix', 'user__first_name')
    )

    zangers = base_qs.filter(role__icontains='zanger')
    zwaaibaas = base_qs.filter(role__icontains='zwaaibaas')
    muzikanten = base_qs.filter(role__icontains='muzikant')

    return {
        'base_qs': base_qs,
        'zangers': zangers,
        'zwaaibaas': zwaaibaas,
        'muzikanten': muzikanten,
    }
