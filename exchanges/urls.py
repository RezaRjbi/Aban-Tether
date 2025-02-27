from django.urls import path

from . import views

urlpatterns = [path("", views.ExchangeList.as_view(), name="exchanges")]
