from django.urls import path, reverse_lazy
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

    path('ledenlijst/', views.members_list, name='members_list'),
    path('ledenlijst/download/', views.members_pdf, name='members_pdf'),

    path(
        'wachtwoord-wijzigen/',
        auth_views.PasswordChangeView.as_view(
            template_name='password_change.html',
            success_url=reverse_lazy('accounts:password_change_done'),
        ),
        name='password_change',
    ),
    path(
        'wachtwoord-wijzigen/klaar/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='password_change_done.html',
        ),
        name='password_change_done',
    ),
]
