from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.index, name="dashboard"),
    path("account-details/", views.account_details, name="account_details"),
    path("statement/", views.statement, name="statement"),
]
