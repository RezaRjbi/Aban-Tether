from django.urls import path

from . import views

urlpatterns = [
    path("otp/send/", views.OTPSendView.as_view(), name="otp_send"),
    path("otp/verify/", views.VerifyOTPView.as_view(), name="otp_verify"),
    path("", views.ListCreateUserView.as_view(), name="list_create_user"),
    path(
        "<int:pk>/",
        views.RetrieveUpdateDeleteUserView.as_view(),
        name="retrieve_delete_update_user",
    ),
]
