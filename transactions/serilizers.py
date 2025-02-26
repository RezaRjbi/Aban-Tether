from rest_framework import serializers

from .models import Balance, Transaction


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ["balance"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ["id", "user"]
        read_only_fields = ["created_at", "type", "reference_number", "tracking_code"]
