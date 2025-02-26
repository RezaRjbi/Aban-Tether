from rest_framework import serializers
from .models import User


class OTPSendSerializer(serializers.Serializer):
    mobile = serializers.RegexField(required=True, regex=r"^9\d{9}$")


class VerifyOTPSerializer(OTPSendSerializer):
    otp = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "mobile"]
