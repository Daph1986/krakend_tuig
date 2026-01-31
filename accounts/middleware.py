from django.shortcuts import redirect
from django.urls import reverse


class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            # 👇 JUISTE NAAM dankzij related_name='member_profile'
            profile = getattr(user, 'member_profile', None)

            if profile and profile.must_change_password:
                allowed_paths = {
                    reverse('accounts:password_change'),
                    reverse('accounts:logout'),
                }

                # Sta static/media toe
                if (
                    request.path.startswith('/static/')
                    or request.path.startswith('/media/')
                ):
                    return self.get_response(request)

                if request.path not in allowed_paths:
                    return redirect('accounts:password_change')

        return self.get_response(request)
