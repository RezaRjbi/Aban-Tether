from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()


class OTPTestCase(APITestCase):
    def setUp(self):
        self.mobile = "9123456789"
        self.otp = "123456"
        self.otp_send_url = "/users/otp/send/"
        self.otp_verify_url = "/users/otp/verify/"

    def test_send_otp_success(self):
        response = self.client.post(self.otp_send_url, {"mobile": self.mobile})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "OTP sent successfully.")
        self.assertTrue(User.objects.filter(mobile=self.mobile).exists())

    def test_verify_otp_success(self):
        user = User.objects.create_user(mobile=self.mobile)
        response = self.client.post(
            self.otp_verify_url, {"mobile": self.mobile, "otp": self.otp}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_verify_otp_failure(self):
        User.objects.create_user(mobile=self.mobile)
        response = self.client.post(
            self.otp_verify_url, {"mobile": self.mobile, "otp": "000000"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_user(mobile=User.ME)
        self.client.force_authenticate(user=self.superuser)
        self.user_list_url = "/users/"
        self.user_detail_url = "/users/{}/".format(self.superuser.id)

    def test_list_users(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        response = self.client.post(self.user_list_url, {"mobile": "9123456780"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(mobile="9123456780").exists())

    def test_retrieve_user(self):
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["mobile"], User.ME)

    def test_update_user(self):
        response = self.client.patch(self.user_detail_url, {"mobile": "9123456781"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.superuser.refresh_from_db()
        self.assertEqual(self.superuser.mobile, "9123456781")

    def test_delete_user(self):
        response = self.client.delete(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.superuser.id).exists())
