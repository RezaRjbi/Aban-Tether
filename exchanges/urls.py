from django.urls import path

from . import views

urlpatterns = [
    path("", views.ExchangeList.as_view(), name="exchanges"),
    path("<int:pk>/", views.ExchangeRetrieveUpdateDestroy.as_view(), name="exchange"),
    path("buy/", views.ExchangeBuyView.as_view(), name="buy"),
    path("sell/", views.ExchangeSellView.as_view(), name="sell"),
]
