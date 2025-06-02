from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import translation


class UserViewsTest(TestCase):
    """Тесты представлений пользователей"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Активируем английскую локализацию для тестов
        translation.activate('en')

    def test_register_view_get(self):
        """Тест GET запроса к странице регистрации"""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        # Проверяем английский текст
        self.assertContains(response, 'Registration')

    def test_register_view_post_valid(self):
        """Тест успешной регистрации"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_post_invalid(self):
        """Тест регистрации с невалидными данными"""
        data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'complexpass123',
            'password2': 'differentpass'
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_login_view_get(self):
        """Тест GET запроса к странице входа"""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        # Проверяем английский текст
        self.assertContains(response, 'Login')

    def test_login_view_post_valid(self):
        """Тест успешной авторизации"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('users:login'), data)
        # Учитываем языковой префикс
        self.assertRedirects(response, '/en/')

    def test_login_view_post_invalid(self):
        """Тест авторизации с неверными данными"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('users:login'), data)
        self.assertEqual(response.status_code, 200)
        # Проверяем английский текст ошибки
        self.assertContains(
            response, 'Please enter a correct username and password')

    def test_logout_view(self):
        """Тест выхода из системы"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('users:logout'))
        # Учитываем языковой префикс
        self.assertRedirects(response, '/en/')
