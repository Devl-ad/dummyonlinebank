from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.encoding import force_str
from django.contrib.auth.forms import SetPasswordForm

from django.core.cache import cache
from account.models import Account

from baseapp import utils

from .forms import RegisterForm, CreateAcctForm, LoginForm


def sign_in(request):
    if request.user.is_authenticated:
        messages.warning(request, ("Already logged in"))
        return redirect("/dashboard")
    destination = utils.get_next_destination(request)
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                if destination:
                    return redirect(f"{destination}")
                else:
                    return redirect("dashboard")
    else:
        form = LoginForm()
    return render(request, "auth/login.html", {"form": form})


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
            cache.set(user["email"], user, timeout=600)
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
    userData = utils.getToken(authToken)
    if request.POST:
        form = CreateAcctForm(request.POST)
        if form.is_valid():
            cache.delete(userData[1])
            instance = form.save()
            current_site = get_current_site(request)
            subject = f"Welcome to {current_site.domain}"
            context = {
                "user": instance,
                "domain": current_site.domain,
            }
            message = get_template("auth/welcome.email.html").render(context)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=utils.EMAIL_ADMIN,
                to=[instance.email],
                reply_to=[utils.EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)
            messages.info(
                request, "Account created successfully Check your mail for information"
            )
            return redirect("login")
    else:
        userData = userData[0]
        initial_data = {"password": userData["password"], "email": userData["email"]}
        form = CreateAcctForm(initial=initial_data)

    return render(request, "auth/sign-upii.html", {"form": form})


def confirm_mail(request):
    return render(request, "auth/confirm-mail.html")


def forgot_password(request):
    if request.POST:
        email = request.POST.get("email")
        account = None
        try:
            account = Account.objects.get(email__exact=email)
        except Account.DoesNotExist:
            account = None
        if account:
            data = cache.get(account.username)
            if data:
                cache.delete(account.username)
            cache.set(account.username, account, timeout=300)
            print(account)
            current_site = get_current_site(request)
            subject = "Reset Your Password"
            context = {
                "user": account,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(account.email)),
            }
            message = get_template("auth/resetpassword.email.html").render(context)
            mail = EmailMessage(
                subject=subject,
                body=message,
                from_email=utils.EMAIL_ADMIN,
                to=[account.email],
                reply_to=[utils.EMAIL_ADMIN],
            )
            mail.content_subtype = "html"
            mail.send(fail_silently=True)

            messages.success(
                request, (" check your mail box for instructions to continue")
            )
            return redirect("confirm_mail")

        else:
            messages.success(request, ("A User with this email does't exist"))
            return redirect("forgot_password")
    return render(request, "auth/forgot-password.html")


def reset_password(
    request,
    uidb64,
):
    is_encoding_correct = False
    email = None

    try:
        email = force_str(urlsafe_base64_decode(uidb64))
        is_encoding_correct = True

    except:
        is_encoding_correct = False

    if is_encoding_correct == False and email is None:
        messages.info(request, "Link is invalid")
        return redirect("forgot_password")

    account = utils.check_user(email, Account)

    if account is None:
        messages.info(request, "Link is invalid")
        return redirect("forgot_password")
    user = cache.get(account.username)

    if user == None:
        messages.info(request, "Link is invalid")
        return redirect("forgot_password")

    if request.POST:
        form = SetPasswordForm(account, request.POST)

        if form.is_valid():
            form.save()
            cache.delete(account.username)
            messages.success(request, ("Your Password has been reset"))
            return redirect("login")

    else:
        form = SetPasswordForm(user=account)
    return render(request, "auth/reset-password.html", {"form": form})
