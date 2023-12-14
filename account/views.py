from django.shortcuts import render


def sign_in(request):
    return render(request, "auth/login.html")


def sign_up(request):
    return render(request, "auth/sign-upi.html")


def createacct(request):
    return render(request, "auth/sign-upii.html")


def confirm_mail(request):
    return render(request, "auth/confirm-mail.html")
