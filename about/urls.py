from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path(_('leer_ons_kennen/'), views.about, name='about'),

]
