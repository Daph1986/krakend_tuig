from django.urls import path
from . import views

app_name = 'liederen'

urlpatterns = [
    path('', views.liedlijst, name='liedlijst'),
    path('pdf/<int:pk>/', views.lied_pdf, name='lied_pdf'),

    path('beheer/', views.lied_manage_list, name='lied_manage_list'),
    path('beheer/nieuw/', views.lied_create, name='lied_create'),
    path('beheer/<int:pk>/bewerken/', views.lied_edit, name='lied_edit'),
    path('beheer/<int:pk>/verwijderen/', views.lied_delete, name='lied_delete'),
]
