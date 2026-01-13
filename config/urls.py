from django.contrib import admin
from django.urls import path, include
from captcha import urls as captcha_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('contact/', include('contact.urls')),
    path('', include('about.urls')),
    path('captcha/', include(captcha_urls)),
]
