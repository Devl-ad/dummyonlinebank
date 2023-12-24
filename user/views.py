from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from baseapp import utils as baseUtils
from .utils import getTxForm
import uuid
from .forms import (
    CreateTXSBSerializer,
    CreateTXOBSerializer,
    CreateTXInSerializer,
    ChangePinForm,
)
from account.models import Account
from .models import Transactions
from django.http import JsonResponse
from django.core.cache import cache
from django.contrib import messages
from django.db.models import Q


@login_required()
def index(request):
    user = request.user
    last_transactions = Transactions.objects.filter(Q(sender=user) | Q(receiver=user))[
        :1
    ]

    return render(request, "user/index.html", {"last_transactions": last_transactions})


@login_required()
def account_details(request):
    return render(request, "user/account-details.html")


@login_required()
def statement(request):
    user = request.user
    transactions = Transactions.objects.filter(Q(sender=user) | Q(receiver=user))
    return render(request, "user/statement.html", {"transactions": transactions})


@login_required()
def statement_details(request, pk):
    user = request.user
    transaction = get_object_or_404(Transactions, pk=pk)
    if transaction.sender == user:
        send = True
    else:
        send = False
    return render(
        request,
        "user/statement-details.html",
        {"transaction": transaction, "send": send},
    )


@login_required()
def domestic_transfer(request):
    user = request.user
    if request.POST:
        form = CreateTXSBSerializer(user, request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if user.balance >= int(form.cleaned_data.get("amount")):
                token = str(uuid.uuid4())
                cache_key = f"confirm_transfer_{token}"
                ben_cache_key = f"benneficiary_name_{token}"
                data = cache.get(cache_key)
                dataii = cache.get(ben_cache_key)
                if data and dataii:
                    cache.delete(cache_key)
                    cache.delete(ben_cache_key)
                cache.set(cache_key, form.cleaned_data, timeout=600)
                cache.set(ben_cache_key, instance.receiver.get_fullname(), timeout=600)

                return redirect("confirm_trx", token)
            else:
                messages.info(request, "Insufficient Funds")
                return redirect("domestic_transfer")

    else:
        form = CreateTXSBSerializer(user, initial={"type": "DO"})
    return render(request, "user/domestic_transfer.html", {"form": form})


@login_required()
def outside_transfer(request):
    user = request.user
    if request.POST:
        form = CreateTXOBSerializer(user, request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if user.balance >= int(form.cleaned_data.get("amount")):
                full_name = f"{instance.interDetail.first_name} {instance.interDetail.last_name}"
                token = str(uuid.uuid4())
                cache_key = f"confirm_transfer_{token}"
                ben_cache_key = f"benneficiary_name_{token}"
                data = cache.get(cache_key)
                dataii = cache.get(ben_cache_key)
                if data and dataii:
                    cache.delete(cache_key)
                    cache.delete(ben_cache_key)
                cache.set(cache_key, form.cleaned_data, timeout=600)
                cache.set(ben_cache_key, full_name, timeout=600)

                return redirect("confirm_trx", token)
            else:
                messages.info(request, "Insufficient Funds")
                return redirect("outside_transfer")
    else:
        form = CreateTXOBSerializer(user, initial={"type": "OB"})
    return render(request, "user/outside_transfer.html", {"form": form})


@login_required()
def inter_transfer(request):
    user = request.user
    if request.POST:
        form = CreateTXInSerializer(user, request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if user.balance >= int(form.cleaned_data.get("amount")):
                full_name = f"{instance.interDetail.first_name} {instance.interDetail.last_name}"
                token = str(uuid.uuid4())
                cache_key = f"confirm_transfer_{token}"
                ben_cache_key = f"benneficiary_name_{token}"
                data = cache.get(cache_key)
                dataii = cache.get(ben_cache_key)
                if data and dataii:
                    cache.delete(cache_key)
                    cache.delete(ben_cache_key)
                cache.set(cache_key, form.cleaned_data, timeout=600)
                cache.set(ben_cache_key, full_name, timeout=600)

                return redirect("confirm_trx", token)
            else:
                messages.info(request, "Insufficient Funds")
                return redirect("inter_transfer")
        print(form.errors)
    else:
        form = CreateTXInSerializer(user, initial={"type": "IN"})
    return render(request, "user/inter_transfer.html", {"form": form})


@login_required()
def reset_pin(request):
    user = request.user
    if request.POST:
        form = ChangePinForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Your security pin has been changed")
            return redirect("dashboard")
        else:
            print(form.errors)
    else:
        form = ChangePinForm(user)
    return render(request, "user/reset-pin.html", {"form": form})


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
    ben_cache_key = f"benneficiary_name_{token}"
    benneficiary_name = cache.get(ben_cache_key)
    cdata = cache.get(cache_key)

    if not cdata and not benneficiary_name:
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
            # print("TX created")
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
            messages.info(request, f"Invalid security pin")
            return redirect("confirm_trx", token)
    else:
        form = formData(user, initial=cdata)
    return render(
        request,
        "user/confirmTrx.html",
        {
            "form": form,
            "amount": cdata["amount"],
            "benneficiary_name": benneficiary_name,
        },
    )
