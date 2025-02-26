from rest_framework.viewsets import ModelViewSet

from abnttr.permissions import IsSuperUserOrReadOnly
from .models import Currency
from .serializers import CurrencySerializer


class CurrencyViewSet(ModelViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    permission_classes = [IsSuperUserOrReadOnly]
