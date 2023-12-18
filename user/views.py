from django.shortcuts import render


def index(request):
    return render(request, "user/index.html")


def account_details(request):
    return render(request, "user/account-details.html")


def statement(request):
    return render(request, "user/statement.html")


def domestic_transfer(request):
    return render(request, "user/domestic_transfer.html")


def outside_transfer(request):
    return render(request, "user/outside_transfer.html")


def inter_transfer(request):
    return render(request, "user/inter_transfer.html")


def reset_pin(request):
    return render(request, "user/reset-pin.html")
