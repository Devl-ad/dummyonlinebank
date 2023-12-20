from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.encoding import force_str

from django.core.cache import cache
from account.models import Account

from baseapp import utils

from .forms import RegisterForm, CreateAcctForm


def sign_in(request):
    return render(request, "auth/login.html")


def sign_up(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            current_site = get_current_site(request)
            subject = f"welcome to Heritage, confirm your email address"
            user = {
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password1"],
            }
            ke_y = cache.get(user["email"])
            if ke_y:
                cache.delete(user["email"])
            cache.set(user["email"], user, timeout=300)
            context = {
                "user": user,
                "domain": current_site.domain,
                "token": urlsafe_base64_encode(force_bytes(user["email"])),
            }
            message = get_template("auth/confirm.mail.html").render(context)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=utils.EMAIL_ADMIN,
                to=[user["email"]],
                reply_to=[utils.EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)

            messages.info(request, "Check your email for further instructions")
            return redirect("confirm_mail")

    else:
        form = RegisterForm()
    return render(request, "auth/sign-upi.html", {"form": form})


def createacct(request):
    authToken = request.GET.get("authToken")
    if authToken is None:
        messages.info(request, "Link is invalid")
        return redirect("register")
    if authToken and not utils.checkToken(authToken):
        messages.info(request, "Link is invalid or has expired")
        return redirect("register")
    if request.POST:
        form = CreateAcctForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            messages.info(request, "Account created successfully")
            return redirect("dashboard")
        else:
            print(form.errors)
    else:
        userData = utils.getToken(authToken)
        print(userData)
        initial_data = {"password": userData["password"], "email": userData["email"]}
        form = CreateAcctForm(initial=initial_data)

    return render(request, "auth/sign-upii.html", {"form": form})


def confirm_mail(request):
    return render(request, "auth/confirm-mail.html")


def forgot_password(request):
    return render(request, "auth/forgot-password.html")


def reset_password(request):
    return render(request, "auth/reset-password.html")
