from django.urls import path
from django.contrib.auth import views as auth_views
import re
from .views import *

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/register_and_login/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/register_and_login/logout.html'), name='logout'),
    path('logout-then-login/', auth_views.logout_then_login, name='logout_then_login'),
    path(
        'password-change/',
        auth_views.PasswordChangeView.as_view(template_name='account/register_and_login/password_change_form.html'),
        name='logout_then_login'),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='account/register_and_login/password_change_done.html'),
        name='logout_then_login'),
    path('password-resert/',
         auth_views.PasswordResetView.as_view(template_name='account/register_and_login/password_reset_form.html'),
         name='password_reset'),
    path('password-resert/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/register_and_login/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/register_and_login/password_reset_confirm'
                                                                   '.html'),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/register_and_login'
                                                                    '/password_reset_complete.html'),
         name='password_reset_complete'),
    path('register/', register, name='register'),
    path('input_data/', input_data, name='input_data'),
    path('address_delete/<int:mainid>/', addres_delete, name='main'),
    path('hostinfo/<int:hostid>/', host_info, name='hostinfo'),
    path('', home, name='home'),
    path('group/', group, name='group'),
]