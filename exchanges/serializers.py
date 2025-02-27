from rest_framework import serializers

from .models import Exchange


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        exclude = ["id", "user"]
        read_only_fields = [
            "currency",
            "fee",
            "quantity",
            "type",
            "created_at",
            "updated_at",
        ]
