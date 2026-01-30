from django.contrib import admin
from django.urls import path, include
from captcha import urls as captcha_urls
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(
        'admin/logout/',
        auth_views.LogoutView.as_view(template_name='registration/logged_out.html'),
        name='admin_logout',
    ),

    path('admin/', admin.site.urls),

    path('', include('about.urls')),
    path('accounts/', include('accounts.urls')),
    path('agenda/', include('agenda.urls')),
    path('captcha/', include(captcha_urls)),
    path('contact/', include('contact.urls')),
    path('liedteksten/', include('liederen.urls', namespace='liederen')),
    path('planning/', include('planning.urls', namespace='planning')),
    path('', include('public_content.urls')),
    path('sponsors/', include('sponsors.urls', namespace='sponsors')),
    path('', include('website.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Handig voor lokaal testen met DEBUG=False
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def custom_permission_denied_view(request, exception=None):
    return render(request, '403.html', status=403)


handler403 = custom_permission_denied_view
