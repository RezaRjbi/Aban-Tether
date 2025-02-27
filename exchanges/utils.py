import time
from dataclasses import dataclass

from decimal import Decimal
from typing import ClassVar

from django.db import transaction
from django.db.models import QuerySet, Sum

from .models import Exchange


def get_currency_fee(currency: str) -> Decimal:
    """this function return dummy data for different currency's price"""
    currencies = {"ABAN": Decimal(4.0), "BTC": Decimal(10)}
    return currencies[currency]


@dataclass(frozen=True)
class TotalAmountResponse:
    total_price: Decimal
    total_quantity: Decimal


class ExchangeManager:
    THRESHOLD: ClassVar[int] = 10

    def __init__(self, currency_id: int, currency_name: str) -> None:
        self.currency_id: int = currency_id
        self.currency_name: str = currency_name
        self.query_set: QuerySet = Exchange.objects.filter(
            currency_id=self.currency_id, state=Exchange.State.PENDING
        ).select_related("currency")

    def update_exchanges(self, state: Exchange.State):
        self.query_set.select_for_update().update(state=state)

    def calculate_total_amount(self) -> TotalAmountResponse:
        total_price = Decimal(
            sum(exchange.quantity * exchange.fee for exchange in self.query_set)
        )
        total_quantity = Decimal(sum(exchange.quantity for exchange in self.query_set))
        return TotalAmountResponse(
            total_price=total_price, total_quantity=total_quantity
        )

    def buy(self) -> bool:
        total_amount = self.calculate_total_amount()
        if total_amount.total_price >= self.THRESHOLD:
            return self.buy_from_exchange(
                self.currency_name, total_amount.total_quantity
            )

    def __call__(self):
        with transaction.atomic():
            bought = self.buy()
            self.update_exchanges(
                Exchange.State.DONE if bought else Exchange.State.CANCELLED
            )

    @staticmethod
    def buy_from_exchange(currency: str, quantity: Decimal) -> bool:
        time.sleep(1)
        print(f"{quantity} {currency} has been bought")
        return True

    @staticmethod
    def calculate_total_asset(currency_id: str, user_id: int) -> Decimal:
        return Exchange.objects.filter(
            currency_id=currency_id,
            user_id=user_id,
            state=Exchange.State.DONE,
            type=Exchange.Type.BUY,
        ).aggregate(total=Sum("quantity", default=0))["total"]
