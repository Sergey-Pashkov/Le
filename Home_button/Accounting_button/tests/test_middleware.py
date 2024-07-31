# Accounting_button/tests/test_middleware.py
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse

class GroupRedirectMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаем группы
        self.owner_group = Group.objects.create(name='Собственник')
        self.organizer_group = Group.objects.create(name='Организатор')
        self.executor_group = Group.objects.create(name='Исполнитель')

        # Создаем пользователей и добавляем их в группы
        self.owner_user = User.objects.create_user(username='owner', password='password')
        self.owner_user.groups.add(self.owner_group)

        self.organizer_user = User.objects.create_user(username='organizer', password='password')
        self.organizer_user.groups.add(self.organizer_group)

        self.executor_user = User.objects.create_user(username='executor', password='password')
        self.executor_user.groups.add(self.executor_group)

    def test_owner_redirect(self):
        self.client.login(username='owner', password='password')
        response = self.client.get('/accounts/profile/')
        self.assertRedirects(response, reverse('Accounting_button:owner_dashboard'))

    def test_organizer_redirect(self):
        self.client.login(username='organizer', password='password')
        response = self.client.get('/accounts/profile/')
        self.assertRedirects(response, reverse('Accounting_button:organizer_dashboard'))

    def test_executor_redirect(self):
        self.client.login(username='executor', password='password')
        response = self.client.get('/accounts/profile/')
        self.assertRedirects(response, reverse('Accounting_button:executor_dashboard'))

    def test_no_redirect_for_unauthenticated_user(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
