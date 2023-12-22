from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from baseapp import utils as baseUtils
from .utils import getTxForm
import uuid
from .forms import CreateTXSBSerializer
from account.models import Account
from django.http import JsonResponse
from django.core.cache import cache
from django.contrib import messages


@login_required()
def index(request):
    # print(utils.get_client_ip(request))
    return render(request, "user/index.html")


@login_required()
def account_details(request):
    return render(request, "user/account-details.html")


@login_required()
def statement(request):
    return render(request, "user/statement.html")


@login_required()
def domestic_transfer(request):
    user = request.user
    if request.POST:
        form = CreateTXSBSerializer(user, request.POST)
        if form.is_valid():
            if user.balance >= int(form.cleaned_data.get("amount")):
                token = str(uuid.uuid4())
                cache_key = f"confirm_transfer_{token}"
                data = cache.get(cache_key)
                if data:
                    cache.delete(cache_key)

                cache.set(cache_key, form.cleaned_data, timeout=600)
                return redirect("confirm_trx", token)
            else:
                messages.info(request, "Insufficient Funds")
                return redirect("domestic_transfer")

    else:
        form = CreateTXSBSerializer(user, initial={"type": "DO"})
    return render(request, "user/domestic_transfer.html", {"form": form})


@login_required()
def outside_transfer(request):
    return render(request, "user/outside_transfer.html")


@login_required()
def inter_transfer(request):
    return render(request, "user/inter_transfer.html")


@login_required()
def reset_pin(request):
    return render(request, "user/reset-pin.html")


def get_ben_name(request):
    account_number = str(request.GET.get("acc_number"))
    context = {}
    try:
        benneficiary = Account.objects.get(username__exact=account_number)
        context["name"] = benneficiary.get_fullname()
        context["id"] = benneficiary.id

    except Account.DoesNotExist:
        context["error"] = True
    return JsonResponse(context)


@login_required()
def confirm_trx(request, token):
    user = request.user
    cache_key = f"confirm_transfer_{token}"
    cdata = cache.get(cache_key)

    if not cdata:
        messages.info(request, "Invalid link")
        return redirect("dashboard")
    if user.balance < int(cdata["amount"]):
        messages.info(request, "SOMETHING WENT WRONG")
        return redirect("dashboard")
    tx_type = cdata["type"]
    formData = getTxForm(tx_type)
    if request.POST:
        security_pin = request.POST.get("security_pin")
        form = formData(user, request.POST)
        if user.security_pin == security_pin:
            print("TX created")
            cache.delete(cache_key)
            if form.is_valid():
                form.save()
                messages.info(
                    request, f"A transaction of ${cdata['amount']} has been created"
                )
                return redirect("dashboard")
            else:
                messages.info(request, "SOMETHING WENT WRONG")
                return redirect("dashboard")

        else:
            print("fuck u")
            messages.info(request, f"Invalid security pin")
            return redirect("confirm_trx", token)
    else:
        form = formData(user, initial=cdata)
    return render(
        request, "user/confirmTrx.html", {"form": form, "amount": cdata["amount"]}
    )
