from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from baseapp import utils
from .forms import CreateTXSBSerializer
from account.models import Account
from django.http import JsonResponse


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
    form = CreateTXSBSerializer(user)
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
