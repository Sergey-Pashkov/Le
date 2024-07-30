import pytest

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class AccountingButtonTests(TestCase):

    def setUp(self):
        # Создаем пользователя для тестирования
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
    
    def test_owner_dashboard_view(self):
        # Тестируем доступ неавторизованного пользователя
        response = self.client.get(reverse('Accounting_button:owner_dashboard'))
        self.assertEqual(response.status_code, 302)  # Перенаправление на страницу входа

        # Логиним пользователя
        self.client.login(username='testuser', password='testpassword')
        
        # Тестируем доступ авторизованного пользователя
        response = self.client.get(reverse('Accounting_button:owner_dashboard'))
        self.assertEqual(response.status_code, 200)  # Успешный доступ
        self.assertTemplateUsed(response, 'Accounting_button/dashboards/owner_dashboard.html')

    def test_organizer_dashboard_view(self):
        # Тестируем доступ неавторизованного пользователя
        response = self.client.get(reverse('Accounting_button:organizer_dashboard'))
        self.assertEqual(response.status_code, 302)  # Перенаправление на страницу входа

        # Логиним пользователя
        self.client.login(username='testuser', password='testpassword')
        
        # Тестируем доступ авторизованного пользователя
        response = self.client.get(reverse('Accounting_button:organizer_dashboard'))
        self.assertEqual(response.status_code, 200)  # Успешный доступ
        self.assertTemplateUsed(response, 'Accounting_button/dashboards/organizer_dashboard.html')

    def test_executor_dashboard_view(self):
        # Тестируем доступ неавторизованного пользователя
        response = self.client.get(reverse('Accounting_button:executor_dashboard'))
        self.assertEqual(response.status_code, 302)  # Перенаправление на страницу входа

        # Логиним пользователя
        self.client.login(username='testuser', password='testpassword')
        
        # Тестируем доступ авторизованного пользователя
        response = self.client.get(reverse('Accounting_button:executor_dashboard'))
        self.assertEqual(response.status_code, 200)  # Успешный доступ
        self.assertTemplateUsed(response, 'Accounting_button/dashboards/executor_dashboard.html')

    def test_custom_login_view(self):
        response = self.client.get(reverse('Accounting_button:login'))
        self.assertEqual(response.status_code, 200)  # Успешный доступ
        self.assertTemplateUsed(response, 'Accounting_button/login.html')

    def test_custom_logout_view(self):
        # Логиним пользователя
        self.client.login(username='testuser', password='testpassword')
        
        # Тестируем выход
        response = self.client.post(reverse('Accounting_button:logout'))
        self.assertEqual(response.status_code, 302)  # Перенаправление после выхода
