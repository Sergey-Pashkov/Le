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



from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from Accounting_button.models import StaffingSchedule, Functions_of_performers, PerformersRates

class StaffingScheduleTestCase(TestCase):
    
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Создаем запись в модели Functions_of_performers
        self.function = Functions_of_performers.objects.create(name='Function1')

        # Создаем запись в модели PerformersRates
        self.rate = PerformersRates.objects.create(name='Rate1', cost_per_minute=2.5)

        # Создаем объект StaffingSchedule
        self.schedule = StaffingSchedule.objects.create(
            name=self.function,
            rate=self.rate,
            quantity=10,
            time_norm=60,
            owner=self.user
        )

    def test_time_fund_calculation(self):
        # Проверяем корректность расчета time_fund
        self.schedule.save()
        self.assertEqual(self.schedule.time_fund, 600)

    def test_wage_fund_calculation(self):
        # Проверяем корректность расчета wage_fund
        self.schedule.save()
        self.assertEqual(self.schedule.wage_fund, 1500.00)

    def test_str_method(self):
        # Проверяем метод __str__
        self.assertEqual(str(self.schedule), 'Function1')

    def test_protect_on_delete(self):
        # Проверяем поведение PROTECT для поля 'name'
        with self.assertRaises(ProtectedError):
            self.function.delete()

        # Проверяем поведение PROTECT для поля 'rate'
        with self.assertRaises(ProtectedError):
            self.rate.delete()

    def test_set_null_on_delete(self):
        # Проверяем поведение SET_NULL для поля 'owner'
        self.user.delete()
        self.schedule.refresh_from_db()
        self.assertIsNone(self.schedule.owner)

from django.test import TestCase
from django.contrib.auth.models import User
from Accounting_button.models import Functions_of_organizers, OrganizersRates

class OrganizersRatesModelTest(TestCase):

    def setUp(self):
        # Создаем пользователя для тестов
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Создаем тестовую функцию организатора
        self.function = Functions_of_organizers.objects.create(
            name='Организатор мероприятия',
            description='Отвечает за организацию и проведение мероприятий.',
            owner=self.user
        )

    def test_create_organizers_rate(self):
        """
        Тестирование создания объекта OrganizersRates.
        """
        rate = OrganizersRates.objects.create(
            name=self.function,
            standard=25.50,
            description='Тестовая ставка',
            owner=self.user
        )
        self.assertEqual(rate.name, self.function)
        self.assertEqual(rate.standard, 25.50)
        self.assertEqual(rate.description, 'Тестовая ставка')
        self.assertEqual(rate.owner, self.user)

    def test_update_organizers_rate(self):
        """
        Тестирование обновления объекта OrganizersRates.
        """
        rate = OrganizersRates.objects.create(
            name=self.function,
            standard=25.50,
            description='Тестовая ставка',
            owner=self.user
        )
        rate.standard = 30.75
        rate.description = 'Обновленная ставка'
        rate.save()
        
        updated_rate = OrganizersRates.objects.get(id=rate.id)
        self.assertEqual(updated_rate.standard, 30.75)
        self.assertEqual(updated_rate.description, 'Обновленная ставка')

    def test_delete_organizers_rate(self):
        """
        Тестирование удаления объекта OrganizersRates.
        """
        rate = OrganizersRates.objects.create(
            name=self.function,
            standard=25.50,
            description='Тестовая ставка',
            owner=self.user
        )
        rate_id = rate.id
        rate.delete()
        
        with self.assertRaises(OrganizersRates.DoesNotExist):
            OrganizersRates.objects.get(id=rate_id)


# test_models.py

from django.test import TestCase
from django.contrib.auth.models import User
from Accounting_button.models import TaxationSystems

class TaxationSystemsModelTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_taxation_system(self):
        # Создаем объект налоговой системы
        taxation_system = TaxationSystems.objects.create(
            name='General Taxation System',
            description='This is a general taxation system.',
            owner=self.user
        )
        # Проверяем, что объект создан
        self.assertEqual(taxation_system.name, 'General Taxation System')
        self.assertEqual(taxation_system.description, 'This is a general taxation system.')
        self.assertEqual(taxation_system.owner, self.user)

    def test_taxation_system_str(self):
        # Создаем объект налоговой системы
        taxation_system = TaxationSystems.objects.create(
            name='General Taxation System',
            description='This is a general taxation system.',
            owner=self.user
        )
        # Проверяем, что метод __str__ возвращает правильное значение
        self.assertEqual(str(taxation_system), 'General Taxation System')
