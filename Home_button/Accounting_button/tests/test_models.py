import pytest

# Accounting_button/tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import User
from Accounting_button.models import Functions_of_performers

class FunctionsOfPerformersTest(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='password')

        # Создаем экземпляр функции исполнителя
        self.function = Functions_of_performers.objects.create(
            name='Test Function',
            description='This is a test function description',
            owner=self.user
        )

    def test_function_creation(self):
        # Проверяем, что экземпляр функции был корректно создан
        self.assertEqual(self.function.name, 'Test Function')
        self.assertEqual(self.function.description, 'This is a test function description')
        self.assertEqual(self.function.owner, self.user)

    def test_function_str_method(self):
        # Проверяем, что метод __str__ возвращает корректное название функции
        self.assertEqual(str(self.function), 'Test Function')

    def test_function_owner_nullable(self):
        # Проверяем, что поле owner может быть пустым (null)
        function_without_owner = Functions_of_performers.objects.create(
            name='Function Without Owner',
            description='This function has no owner'
        )
        self.assertIsNone(function_without_owner.owner)
