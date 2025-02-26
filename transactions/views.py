import uuid

from django.db import transaction
from django.db.models import F
from rest_framework import permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Balance, Transaction
from .serilizers import BalanceSerializer, TransactionSerializer


class BalanceView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BalanceSerializer

    def get_object(self):
        return self.request.user.balance


class TransactionView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class DepositView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            user_balance: Balance = (
                Balance.objects.filter(user=self.request.user)
                .select_for_update()
                .first()
            )
            additional_deposit_data = {
                "type": Transaction.Type.DEPOSIT,
                "reference_number": str(uuid.uuid4()),
                "tracking_code": str(uuid.uuid4()),
                "user": self.request.user,
            }

            user_balance.balance = F("balance") + serializer.validated_data["amount"]
            user_balance.save()
            serializer.save(**additional_deposit_data)
