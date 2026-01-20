from django.contrib import admin
from django.urls import path, include
from captcha import urls as captcha_urls
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('contact/', include('contact.urls')),
    path('', include('about.urls')),
    path('captcha/', include(captcha_urls)),
    path('agenda/', include('agenda.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('public_content.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


def custom_permission_denied_view(request, exception=None):
    return render(request, '403.html', status=403)


handler403 = custom_permission_denied_view
