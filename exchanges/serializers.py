from decimal import Decimal

from rest_framework import serializers

from .models import Exchange


class ExchangeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        exclude = ["user"]


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        exclude = ["user"]
        read_only_fields = [
            "id",
            "currency",
            "fee",
            "quantity",
            "type",
            "created_at",
            "updated_at",
        ]


class ExchangeBuySerializer(serializers.Serializer):
    currency = serializers.CharField()
    quantity = serializers.DecimalField(
        max_digits=10, decimal_places=4, min_value=Decimal()
    )


class ExchangeSellSerializer(serializers.ModelSerializer):
    currency = serializers.CharField()

    class Meta:
        model = Exchange
        exclude = ["user"]
        read_only_fields = ["fee", "type"]
