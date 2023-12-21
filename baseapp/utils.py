import random
from django.conf import settings
from django.utils import timezone
from uuid import uuid4
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core.cache import cache


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def gen_random_number():
    return str(random.randint(1000000000, 9999999999))


EMAIL_ADMIN = settings.DEFAULT_FROM_EMAIL
D = "deposite"
W = "withdraw"


def get_next_destination(request):
    next = None
    if request.GET.get("next"):
        next = str(request.GET.get("next"))
    return next


def ref_code():
    code = str(uuid4()).replace(" ", "-").upper()[:8]
    return code


STATUS = {
    "PENDING": "PENDING",
    "SUCCESS": "SUCCESS",
    "DECLINED": "DECLINED",
}

TX_TYPE = {"LO": "Local transfer", "DO": "Domestic transfer", "IN": "International"}


def alertTx(transaction, current_site, subject, status, to_email, name):
    context = {
        "name": name,
        "domain": current_site.domain,
        "tx": transaction,
        "ty_pe": status,
    }
    message = get_template("superuser/txprocess.email.html").render(context)
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=EMAIL_ADMIN,
        to=[to_email],
        reply_to=[EMAIL_ADMIN],
    )
    mail.content_subtype = "html"
    mail.send(fail_silently=True)


def checkToken(token):
    ke_y = None
    try:
        ke_y = force_str(urlsafe_base64_decode(token))
    except:
        ke_y = None
    if ke_y is not None:
        data = cache.get(ke_y)
        if data:
            return True
    return False


def getToken(verifyToken):
    """
    This fuction must be called only when the token has been verified
    """

    ke_y = force_str(urlsafe_base64_decode(verifyToken))

    data = cache.get(ke_y)

    return [data, ke_y]


def check_user(email, model):
    account = None
    try:
        account = model.objects.get(email__exact=email)
    except model.DoesNotExist:
        account = None

    return account
