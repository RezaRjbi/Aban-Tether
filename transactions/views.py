from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Balance, Transaction
from .serilizers import BalanceSerializer


class BalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BalanceSerializer

    def get(self, request):
        return Response(self.serializer_class(instance=request.user.balance).data)
