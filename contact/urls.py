from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact'),
    path('bewerken/', views.contact_edit, name='contact_edit'),
]
