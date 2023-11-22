from django.urls import path, include
from . import views
from .views import *
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .forms import EmailValidationOnForgotPassword



app_name = "users"

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('profile/<str:username>/settings', views.edit_profile_view, name='edit_profile'),
    path('password-reset/',
         PasswordResetView.as_view(
            form_class= EmailValidationOnForgotPassword,
            template_name='users/password_reset.html',
            html_email_template_name='users/password_reset_email.html'),
            name='password-reset'
        ),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/<str:username>/settings/change-email', views.change_email_view, name='change_email_address'),
    path('change_email/<str:username>/<uidb64>/<token>', views.ChangeEmailConfirmation, name='change_email_mail'),
    path('profile/<str:username>/tierlist', TierlistOwned.as_view(), name='tierlist-owned'),
    path('profile/<str:username>/tierlist/delete/<int:id>', views.DeleteTierlist_Profile, name='delete-tierlist-profile'),
    path('profile/<str:username>/tierlist/edit/<int:id>', views.EditTierlist_Profile, name='edit-tierlist-profile'),
    path('profile/<str:username>/templates', TemplatesOwned.as_view(), name='templates-owned'),
    path('profile/<str:username>/templates/edit/<int:id>', views.EditTemplates_Profile, name='edit-templates-profile'),
    path('profile/<str:username>/templates/delete/<int:id>', views.DeleteTemplates_Profile, name='delete-templates-profile'),
]