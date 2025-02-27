from django.db import transaction
from django.db.models import F
from django.http import Http404
from rest_framework import generics, permissions, views
from rest_framework.exceptions import ValidationError

from rest_framework.response import Response

from abnttr.http_exceptions import BadRequestException
from currencies.models import Currency
from transactions.models import Balance

from .models import Exchange
from .permissions import IsUpdateAllowed
from .serializers import (
    ExchangeSerializer,
    ExchangeUpdateSerializer,
    ExchangeBuySerializer,
)
from .utils import get_currency_fee, ExchangeManager


class ExchangeList(generics.ListAPIView):
    serializer_class = ExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Exchange.objects.filter(user=self.request.user)


class ExchangeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExchangeUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsUpdateAllowed]

    def get_queryset(self):
        return Exchange.objects.filter(user=self.request.user)

class ExchangeBuyView(views.APIView):
    serializer_class = ExchangeBuySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        currency: Currency = (
            Currency.objects.filter(
                name=serializer.validated_data["currency"], is_active=True
            )
            .only("id", "name")
            .first()
        )
        if not currency:
            raise Http404("Currency does not exist")
        currency_fee = get_currency_fee(currency.name)
        total_price = serializer.validated_data["quantity"] * currency_fee
        with transaction.atomic():
            user_balance_update = Balance.objects.filter(
                user=request.user, balance__gte=total_price
            ).update(balance=F("balance") - total_price)
            if not user_balance_update:
                raise BadRequestException("Insufficient balance")
            exchange = Exchange.objects.create(
                user=request.user,
                currency_id=currency.id,
                fee=currency_fee,
                quantity=serializer.validated_data["quantity"],
                type=Exchange.Type.BUY,
            )
            exchange_manager = ExchangeManager(currency.id, currency.name)
            transaction.on_commit(exchange_manager)
            return Response(ExchangeSerializer(instance=exchange).data, status=201)
