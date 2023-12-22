from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from baseapp import utils


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
    return render(request, "user/domestic_transfer.html")


@login_required()
def outside_transfer(request):
    return render(request, "user/outside_transfer.html")


@login_required()
def inter_transfer(request):
    return render(request, "user/inter_transfer.html")


@login_required()
def reset_pin(request):
    return render(request, "user/reset-pin.html")
