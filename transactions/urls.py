from django.urls import path
from . import views

urlpatterns = [
    path("balance/", views.BalanceView.as_view(), name="balance"),
    path("statement/", views.TransactionView.as_view(), name="transactions"),
    path("deposit/", views.DepositView.as_view(), name="deposit"),
]
