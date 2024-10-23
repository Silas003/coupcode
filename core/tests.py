from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from django.test import TestCase
from core.serializers import BetSerializer, HistorySerializer
from core.models import Bet, History
from accounts.models import *

class TestBetSerializer(TestCase):
    def setUp(self):
       
        self.user=CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
        )

    def test_valid_data(self):
        data = {

            "selection": "HEAD",
            "stake": 10.0,
            "user": self.user.pk,
        }
        serializer=BetSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        data = {

            "result": "test_result",
            "selection": "test_selection",
            "stake": 10.0,
            "user": 1,
        }
        serializer=BetSerializer(data=data)
        self.assertFalse(serializer.is_valid())




class TestBetView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("core:bet-list")
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
        )

    def test_bet_creation(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "selection": "HEAD",
            "stake": 10.0,
            "user": self.user.pk,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bet_creation_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "selection": "TAIL",
            "stake": -10.0,
            "user": "invalid user",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestHistoryView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("core:history-list")
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
        )

        self.bet=Bet.objects.create(
            user=self.user,
            stake=10.0,
            selection="HEAD",
        )
    def test_history_creation(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "user": self.user.pk,
            "previous_bets":[self.bet.pk]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

