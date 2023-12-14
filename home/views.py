from django.shortcuts import render


def home(request):
    return render(request, "home/index.html")


def about(request):
    return render(request, "home/about.html")


def services(request):
    return render(request, "home/services.html")


def loan(request):
    return render(request, "home/loan.html")


def contact(request):
    return render(request, "home/contact.html")
