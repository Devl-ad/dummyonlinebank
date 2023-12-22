from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.index, name="dashboard"),
    path("account-details/", views.account_details, name="account_details"),
    path("transactions-log/", views.statement, name="statement"),
    path("domestic-transfer/", views.domestic_transfer, name="domestic_transfer"),
    path("other-transfer/", views.outside_transfer, name="outside_transfer"),
    path("international-transfer/", views.inter_transfer, name="inter_transfer"),
    path("reset-pin/", views.reset_pin, name="reset_pin"),
    path("get-benneficiary/", views.get_ben_name, name="get_ben_name"),
]
