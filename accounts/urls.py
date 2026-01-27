from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login',
    ),
    path('logout/', views.logout_view, name='logout'),

    path('profiel/', views.profile_detail, name='profile_detail'),
    path('profiel/bewerken/', views.profile_edit, name='profile_edit'),
]
