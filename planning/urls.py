from django.urls import path
from . import views

app_name = 'planning'

urlpatterns = [
    path('', views.planning_overzicht, name='overzicht'),
    path('status/', views.planning_status_update, name='status_update'),
    path('optreden/nieuw/', views.optreden_create, name='optreden_create'),
    path('optreden/<int:pk>/bewerken/', views.optreden_update, name='optreden_update'),
    path('optreden/<int:pk>/verwijderen/', views.optreden_delete, name='optreden_delete'),
]
