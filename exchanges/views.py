from rest_framework import generics, permissions

from .models import Exchange
from .serializers import ExchangeSerializer


class ExchangeList(generics.ListAPIView):
    serializer_class = ExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Exchange.objects.filter(user=self.request.user)
