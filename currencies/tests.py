from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Currency

User = get_user_model()

class CurrencyAPITestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_user(mobile=User.ME)
        self.user = User.objects.create_user(mobile="9123456789")
        self.currency = Currency.objects.create(
            name="BTC", display_name="Bitcoin", symbol="₿", is_active=True
        )
        self.currency_list_url = "/currencies/"
        self.currency_detail_url = f"/currencies/{self.currency.id}/"

    def test_list_currencies(self):
        response = self.client.get(self.currency_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_currency(self):
        response = self.client.get(self.currency_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "BTC")

    def test_create_currency_as_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        print(self.superuser.is_superuser)
        response = self.client.post(
            self.currency_list_url,
            {"name": "tether", "display_name": "Tether", "symbol": "₮", "is_active": True},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Currency.objects.filter(name="tether").exists())

    def test_create_currency_as_regular_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.currency_list_url,
            {"name": "tether", "display_name": "Tether", "symbol": "₮", "is_active": True},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_currency_as_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.patch(self.currency_detail_url, {"name": "BTC2.0"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.currency.refresh_from_db()
        self.assertEqual(self.currency.name, "BTC2.0")

    def test_update_currency_as_regular_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.currency_detail_url, {"name": "BTC modified"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_currency_as_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.currency_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Currency.objects.filter(id=self.currency.id).exists())

    def test_delete_currency_as_regular_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.currency_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)