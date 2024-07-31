# Accounting_button/tests/test_views.py

import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import get_user_model
from Accounting_button.models import Functions_of_performers

class AccountingButtonTests(TestCase):

    def setUp(self):
        # Создаем пользователя для тестирования
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.user.user_permissions.add(Permission.objects.get(codename='add_functions_of_performers'))
        self.user.user_permissions.add(Permission.objects.get(codename='view_functions_of_performers'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_functions_of_performers'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_functions_of_performers'))
        
        # Создаем группу и добавляем пользователя в группу
        self.group = Group.objects.create(name='Собственник')
        self.user.groups.add(self.group)

        # Создаем тестовую функцию исполнителя
        self.function = Functions_of_performers.objects.create(
            name='Test Function',
            description='This is a test function description',
            owner=self.user
        )
    
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

    def test_create_function_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('Accounting_button:create_function'), {
            'name': 'New Function',
            'description': 'New function description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Functions_of_performers.objects.filter(name='New Function').exists())

    def test_read_function_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('Accounting_button:read_function', args=[self.function.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/functions_of_performers/function_detail.html')
        self.assertContains(response, self.function.name)

    def test_update_function_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('Accounting_button:update_function', args=[self.function.id]), {
            'name': 'Updated Function',
            'description': 'Updated function description'
        })
        self.assertEqual(response.status_code, 302)
        self.function.refresh_from_db()
        self.assertEqual(self.function.name, 'Updated Function')

    def test_delete_function_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('Accounting_button:delete_function', args=[self.function.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Functions_of_performers.objects.filter(id=self.function.id).exists())

    def test_functions_list_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('Accounting_button:functions_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/functions_of_performers/functions_list.html')
        self.assertContains(response, self.function.name)
