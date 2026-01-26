from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('', views.home, name='home'),
    path(_('homepage/bewerken/'), views.homepage_edit, name='homepage_edit'),
    path(_('homepage/slides/'), views.home_slides_list, name='home_slides_list'),
    path(_('homepage/slides/nieuw/'), views.home_slide_create, name='home_slide_create'),
    path(_('homepage/slides/<int:pk>/bewerken/'), views.home_slide_update, name='home_slide_update'),
    path(_('homepage/slides/<int:pk>/verwijderen/'), views.home_slide_delete, name='home_slide_delete'),
    path(_('zing_mee/'), views.zing_mee, name='zing_mee'),
    path('beheer/zing-mee/', views.zing_mee_edit, name='zing_mee_edit'),
]
