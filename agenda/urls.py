from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('', views.agenda, name='overzicht'),
    path('nieuw/', views.optreden_create, name='optreden_create'),
    path('<int:pk>/wijzig/', views.optreden_update, name='optreden_update'),
    path('<int:pk>/verwijder/', views.optreden_delete, name='optreden_delete'),
]
