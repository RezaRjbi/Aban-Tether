from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from .models import Exchange
from .serializers import ExchangeSerializer


class ExchangeList(generics.ListAPIView):
    serializer_class = ExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Exchange.objects.filter(user=self.request.user)


class ExchangeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def is_update_allowed(exchange: Exchange, raise_: bool = True) -> bool:
        allowed = exchange.state == Exchange.State.PENDING
        if not allowed and raise_:
            raise ValidationError("only pending exchanges could be cancelled")
        return allowed

    def get_object(self) -> Exchange:
        instance = super().get_object().filter(user=self.request.user)
        if self.request.method not in permissions.SAFE_METHODS:
            self.is_update_allowed(instance, raise_=True)
        return instance
