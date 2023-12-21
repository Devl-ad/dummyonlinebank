from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.sign_in, name="login"),
    path("logout/", views.sign_out, name="logout"),
    path("sign-up/", views.sign_up, name="register"),
    path("create-account/", views.createacct, name="createacct"),
    path("confirm-mail/", views.confirm_mail, name="confirm_mail"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/<uidb64>/", views.reset_password, name="reset_password"),
]
