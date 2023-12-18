from django.shortcuts import render


def index(request):
    return render(request, "user/index.html")


def account_details(request):
    return render(request, "user/account-details.html")


def statement(request):
    return render(request, "user/statement.html")