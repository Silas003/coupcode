from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import CustomUser as User
from .serializers import *
# Create your tests here.
class TestUserCreationView(TestCase):

    def setUp(self):
        self.client=APIClient()
        self.url=reverse("accounts:register-list")
    def test_user_creation(self):
        data = {
            "email": "test@example.com",
            "password": "password123",
            "username": "John",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'],'test@example.com')
        self.assertEqual(response.data['username'],'John')

    def test_user_creation_invalid_data(self):
        data = {
            "email": "invalid_email",
            "password": "password123",
            "username": "John",

        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestVerifyAccountView(TestCase):
    def setUp(self):
        self.url=reverse("accounts:verify-list")
        self.client=APIClient()
        self.user=User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            otp="123456"
        )
    def test_verify_account(self):
        data = {
            "email": "testuser@example.com",
            "otp": "123456"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_account_invalid_data(self):
        data = {
            "email": "invalid_email",
            "otp": "123456"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestResendOtpView(TestCase):
    def setUp(self):
        self.client =APIClient()
        self.url=reverse("accounts:resendotp-list")
        self.user=User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            otp="123456"
        )
    def test_resend_otp(self):
        data = {
            "email": "testuser@example.com"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resend_otp_invalid_data(self):
        data = {
            "email": "invalid_email"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestResetPasswordOtpView(TestCase):
    def setUp(self):
        self.client =APIClient()
        self.url=reverse("accounts:resetotp-list")
        self.user=User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            otp="123456"
        )
    def test_reset_password_otp(self):
        data = {
            "email": "testuser@example.com"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_otp_invalid_data(self):
        data = {
            "email": "invalid_email"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestResetPasswordView(TestCase):
    def setUp(self):
        self.client =APIClient()
        self.url=reverse("accounts:reset-list")
        self.user=User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            otp="123456"
        )
    def test_reset_password(self):
        data = {
            "email": "testuser@example.com",
            "password": "new_password",
            "otp": "123456"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_invalid_data(self):
        data = {
            "email": "invalid_email",
            "password": "new_password"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestLoginView(TestCase):
    def setUp(self):
        self.client =APIClient()
        self.url=reverse("accounts:login")
        self.user=User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            otp="123456"
        )
    
    def test_login(self):
        data = {
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_data(self):
        data = {
            "email": "invalid_email",
            "password": "password123"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class TestUserCreationSerializer(TestCase):
    def setUp(self):
        self.serializer = UserCreationSerializer()

    def test_valid_data(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        self.assertTrue(self.serializer.is_valid(data))

    def test_invalid_data(self):
        data = {
            "username": "",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        self.assertFalse(self.serializer.is_valid(data))

class TestUserViewSerializer(TestCase):
    def setUp(self):
        self.serializer = UserViewSerializer()

    def test_valid_data(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        data = self.serializer.to_representation(user)
        self.assertEqual(data["username"], user.username)
        self.assertEqual(data["email"], user.email)
        self.assertEqual(data["is_active"], user.is_active)

class TestVerifyAccountSerializer(TestCase):
    def setUp(self):
        self.serializer = VerifyAccountSerializer()

    def test_valid_data(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        user.otp = "123456"
        user.save()
        data = {
            "email": user.email,
            "otp": user.otp
        }
        self.assertTrue(self.serializer.is_valid(data))

    def test_invalid_data(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        user.otp = "123456"
        user.save()
        data = {
            "email": user.email,
            "otp": "wrong_otp"
        }
        self.assertFalse(self.serializer.is_valid(data))

class TestResendOtpSerializer(TestCase):
    def setUp(self):
        self.serializer = ResendOtpSerializer()

    def test_valid_data(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        data = {
            "email": user.email
        }
        self.assertTrue(self.serializer.is_valid(data))

    def test_invalid_data(self):
        data = {
            "email": "wrong_email"
        }
        self.assertFalse(self.serializer.is_valid(data))

class TestResetPasswordSerializer(TestCase):
    def setUp(self):
        self.serializer = ResetPasswordSerializer()

    def test_valid_data(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        user.otp = "123456"
        user.save()
        data = {
            "email": user.email,
            "password": "new_password",
            "otp": user.otp
        }
        self.assertTrue(self.serializer.is_valid(data))

    def test_invalid_data(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        user.otp = "123456"
        user.save()
        data = {
            "email": user.email,
            "password": "new_password",
            "otp": "wrong_otp"
        }
        self.assertFalse(self.serializer.is_valid(data))

class TestResetPasswordOtpSerializer(TestCase):
    def setUp(self):
        self.serializer = ResetPasswordOtpSerializer()

    def test_valid_data(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        data = {
            "email": user.email
        }
        self.assertTrue(self.serializer.is_valid(data))

    def test_invalid_data(self):
        data = {
            "email": "wrong_email"
        }
        self.assertFalse(self.serializer.is_valid(data))

class TestProfileSerializer(TestCase):
    def setUp(self):
        self.serializer = ProfileSerializer()

    def test_valid_data(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        profile = Profile.objects.create(
            user=user,
            display_name="test_display_name"
        )
        data = self.serializer.to_representation(profile)
        self.assertEqual(data["display_name"], profile.display_name)

    def test_invalid_data(self):
        data = {
            "display_name": ""
        }
        self.assertFalse(self.serializer.is_valid(data))

class TestLoginSerializer(TestCase):
    def setUp(self):
        self.serializer = LoginSerializer()

    def test_valid_data(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        data = {
            "email": user.email,
            "password": "testpassword"
        }
        self.assertTrue(self.serializer.is_valid(data))

    def test_invalid_data(self):
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        data = {
            "email": user.email,
            "password": "wrong_password"
        }
        self.assertFalse(self.serializer.is_valid(data))

