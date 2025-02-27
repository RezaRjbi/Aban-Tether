from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from rest_framework import status
from transactions.models import Balance
from currencies.models import Currency
from .models import Exchange

User = get_user_model()


class ExchangeAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(mobile=User.ME)
        self.balance = self.user.balance
        Balance.objects.update(balance=100)
        self.client.force_authenticate(user=self.user)
        self.currency = Currency.objects.create(
            name="BTC", symbol="B", display_name="Bitcoin"
        )
        self.exchange = Exchange.objects.create(
            user=self.user,
            currency=self.currency,
            fee=10,
            quantity=2,
            type=Exchange.Type.BUY,
            state=Exchange.State.DONE,
        )
        self.exchange_list_url = "/exchanges/"
        self.exchange_retrieve_url = "/exchanges/{}/"
        self.exchange_buy_url = "/exchanges/buy/"
        self.exchange_sell_url = "/exchanges/sell/"

    def test_get_exchange_list(self):
        response = self.client.get(self.exchange_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exchange_buy_success(self):
        data = {"currency": "BTC", "quantity": 5}
        response = self.client.post(self.exchange_buy_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.balance.refresh_from_db()
        self.assertLess(self.balance.balance, 1000)

    def test_exchange_buy_insufficient_balance(self):
        data = {"currency": "BTC", "quantity": 100}
        response = self.client.post(self.exchange_buy_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exchange_sell_success(self):
        data = {"currency": "BTC", "quantity": 1}
        response = self.client.post(self.exchange_sell_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_exchange_sell_insufficient_asset(self):
        data = {"currency": "BTC", "quantity": 50}
        response = self.client.post(self.exchange_sell_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_exchange_buy_invalid_currency(self):
        data = {"currency": "INVALID", "quantity": 1}
        response = self.client.post(self.exchange_buy_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
