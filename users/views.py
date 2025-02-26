from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .otp_manager import OTP
from .models import User
from .serializers import OTPSendSerializer, VerifyOTPSerializer, UserSerializer
from abnttr.permissions import IsSuperUser

from abnttr import http_exceptions


class OTPSendView(APIView):
    serializer_class = OTPSendSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]
        otp_manager = OTP(mobile)
        User.objects.get_or_create(mobile=mobile)
        if otp_manager.send(mobile):
            return Response({"message": "OTP sent successfully."}, status=200)
        raise http_exceptions.TooManyRequestsException


class VerifyOTPView(APIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]
        otp = serializer.validated_data["otp"]
        user = get_object_or_404(User, mobile=mobile)
        otp_manager = OTP(mobile)
        if otp_manager.verify(mobile, otp):
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=200)
        raise http_exceptions.UnauthorizedException


class ListCreateUserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsSuperUser]


class RetrieveUpdateDeleteUserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsSuperUser]
