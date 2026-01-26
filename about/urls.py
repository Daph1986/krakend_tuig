from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'about'

urlpatterns = [
    path(_('leer_ons_kennen/'), views.about_page, name='about_page'),
    path('beheer/leer-ons-kennen/', views.about_intro_edit, name='about_intro_edit'),
]
