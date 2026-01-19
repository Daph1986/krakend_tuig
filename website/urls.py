from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('', views.home, name='home'),
    path(_('zing_mee/'), views.zing_mee, name='zing_mee'),
]
