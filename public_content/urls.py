from django.urls import path
from . import views

app_name = 'public_content'

urlpatterns = [
    path('fotos-en-videos/', views.media_overview, name='overview'),
    path('fotos-en-videos/albums/<slug:slug>/', views.album_detail, name='album_detail'),
    # path('smoelenboek/', views.smoelenboek_public, name='smoelenboek_public'),
    path('leden/smoelenboek/', views.smoelenboek_private, name='smoelenboek_private'),
    path('videos/', views.videos_list, name='videos_list'),
    path('albums/', views.albums_list, name='albums_list'),

    # management
    path('leden/media/', views.media_manage_home, name='media_manage_home'),

    path('leden/media/albums/', views.album_manage_list, name='album_manage_list'),
    path('leden/media/albums/nieuw/', views.album_create, name='album_create'),
    path('leden/media/albums/<int:pk>/wijzig/', views.album_update, name='album_update'),
    path('leden/media/albums/<int:pk>/verwijder/', views.album_delete, name='album_delete'),

    path('leden/media/albums/<int:album_id>/fotos/nieuw/', views.albumphoto_create, name='albumphoto_create'),
    path('leden/media/fotos/<int:pk>/wijzig/', views.albumphoto_update, name='albumphoto_update'),
    path('leden/media/fotos/<int:pk>/verwijder/', views.albumphoto_delete, name='albumphoto_delete'),

    path('leden/media/videos/', views.video_manage_list, name='video_manage_list'),
    path('leden/media/videos/nieuw/', views.video_create, name='video_create'),
    path('leden/media/videos/<int:pk>/wijzig/', views.video_update, name='video_update'),
    path('leden/media/videos/<int:pk>/verwijder/', views.video_delete, name='video_delete'),
]
