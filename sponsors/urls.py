from django.urls import path
from . import views

app_name = 'sponsors'

urlpatterns = [
    path('', views.sponsoren, name='sponsoren'),
    path('beheer/', views.sponsor_beheer, name='beheer'),
    path('nieuw/', views.sponsor_toevoegen, name='nieuw'),
    path('<int:pk>/bewerk/', views.sponsor_bewerken, name='bewerk'),
    path('<int:pk>/verwijder/', views.sponsor_verwijderen, name='verwijder'),
]
