from django.urls import path
from . import views

app_name = 'public_content'

urlpatterns = [
    path('fotos-en-videos/', views.media_overview, name='overview'),
    path('fotos-en-videos/albums/<slug:slug>/', views.album_detail, name='album_detail'),
    path('smoelenboek/', views.smoelenboek_public, name='smoelenboek_public'),
    path('leden/smoelenboek/', views.smoelenboek_private, name='smoelenboek_private'),
]
