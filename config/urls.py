from django.contrib import admin
from django.urls import path, include
from captcha import urls as captcha_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('contact/', include('contact.urls')),
    path('', include('about.urls')),
    path('captcha/', include(captcha_urls)),
    path('agenda/', include('agenda.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
