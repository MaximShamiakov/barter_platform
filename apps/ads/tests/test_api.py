from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Ad


class AdAPITest(APITestCase):
    """Тесты API для объявлений"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Test description',
            category='electronics',
            condition='new'
        )

    def test_api_ads_list(self):
        """Тест API списка объявлений"""
        url = reverse('api:ads:ad-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # API возвращает пагинированные данные
        if 'results' in response.data:
            # Пагинированный ответ
            ads_data = response.data['results']
        else:
            # Непагинированный ответ
            ads_data = response.data

        self.assertTrue(any(ad['title'] == 'Test Ad' for ad in ads_data))

    def test_api_register(self):
        """Тест API регистрации"""
        url = reverse('api:auth:register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_api_register_password_mismatch(self):
        """Тест API регистрации с несовпадающими паролями"""
        url = reverse('api:auth:register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'differentpass'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_api_login(self):
        """Тест API авторизации"""
        url = reverse('api:auth:login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_login_invalid_credentials(self):
        """Тест API авторизации с неверными данными"""
        url = reverse('api:auth:login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
