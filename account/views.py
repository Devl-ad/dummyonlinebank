from django.shortcuts import render


def sign_in(request):
    return render(request, "auth/login.html")


def sign_up(request):
    return render(request, "auth/sign-upi.html")


def createacct(request):
    return render(request, "auth/sign-upii.html")


def confirm_mail(request):
    return render(request, "auth/confirm-mail.html")


def forgot_password(request):
    return render(request, "auth/forgot-password.html")


def reset_password(request):
    return render(request, "auth/reset-password.html")
