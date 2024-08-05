import pytest

# Accounting_button/tests/test_forms.py
from django.test import TestCase
from Accounting_button.forms import FunctionsOfPerformersForm, PerformersRatesForm

class FunctionsOfPerformersFormTests(TestCase):

    def test_valid_form(self):
        # Данные для создания корректной формы
        data = {
            'name': 'Function 1',
            'description': 'Description of Function 1',
        }
        form = FunctionsOfPerformersForm(data=data)
        self.assertTrue(form.is_valid())  # Форма должна быть валидной

    def test_invalid_form_missing_name(self):
        # Данные для создания некорректной формы (отсутствует поле name)
        data = {
            'description': 'Description of Function 1',
        }
        form = FunctionsOfPerformersForm(data=data)
        self.assertFalse(form.is_valid())  # Форма должна быть невалидной

    def test_invalid_form_missing_description(self):
        # Данные для создания некорректной формы (отсутствует поле description)
        data = {
            'name': 'Function 1',
        }
        form = FunctionsOfPerformersForm(data=data)
        self.assertFalse(form.is_valid())  # Форма должна быть невалидной

class PerformersRatesFormTests(TestCase):

    def test_valid_form(self):
        # Данные для создания корректной формы
        data = {
            'name': 'Rate 1',
            'cost_per_minute': 1.50,
        }
        form = PerformersRatesForm(data=data)
        self.assertTrue(form.is_valid())  # Форма должна быть валидной

    def test_invalid_form_missing_name(self):
        # Данные для создания некорректной формы (отсутствует поле name)
        data = {
            'cost_per_minute': 1.50,
        }
        form = PerformersRatesForm(data=data)
        self.assertFalse(form.is_valid())  # Форма должна быть невалидной

    def test_invalid_form_negative_cost(self):
        # Данные для создания некорректной формы (отрицательное значение стоимости)
        data = {
            'name': 'Rate 1',
            'cost_per_minute': -1.50,
        }
        form = PerformersRatesForm(data=data)
        self.assertFalse(form.is_valid())  # Форма должна быть невалидной

if __name__ == "__main__":
    TestCase.main()


from django.test import TestCase
from Accounting_button.forms import StaffingScheduleForm
from Accounting_button.models import StaffingSchedule, Functions_of_performers, PerformersRates
from django.contrib.auth.models import User

class StaffingScheduleFormTestCase(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Создаем запись в модели Functions_of_performers
        self.function = Functions_of_performers.objects.create(name='Function1')

        # Создаем запись в модели PerformersRates
        self.rate = PerformersRates.objects.create(name='Rate1', cost_per_minute=2.5)

    def test_form_fields(self):
        # Создаем экземпляр формы
        form = StaffingScheduleForm()

        # Проверяем, что форма содержит ожидаемые поля
        self.assertIn('name', form.fields)
        self.assertIn('rate', form.fields)
        self.assertIn('quantity', form.fields)
        self.assertIn('time_norm', form.fields)

    def test_form_valid_data(self):
        # Данные для формы
        form_data = {
            'name': self.function.id,
            'rate': self.rate.id,
            'quantity': 10,
            'time_norm': 60
        }
        form = StaffingScheduleForm(data=form_data)
        
        # Проверяем, что форма валидна
        self.assertTrue(form.is_valid())
        
        # Сохраняем форму и проверяем, что данные были сохранены правильно
        schedule = form.save(commit=False)
        schedule.owner = self.user
        schedule.save()
        
        self.assertEqual(schedule.name, self.function)
        self.assertEqual(schedule.rate, self.rate)
        self.assertEqual(schedule.quantity, 10)
        self.assertEqual(schedule.time_norm, 60)
        self.assertEqual(schedule.time_fund, 600)
        self.assertEqual(schedule.wage_fund, 1500.00)

    def test_form_invalid_data(self):
        # Неполные данные для формы
        form_data = {
            'name': '',
            'rate': self.rate.id,
            'quantity': 10,
            'time_norm': 60
        }
        form = StaffingScheduleForm(data=form_data)
        
        # Проверяем, что форма не валидна
        self.assertFalse(form.is_valid())
        
        # Проверяем наличие ошибки для поля 'name'
        self.assertIn('name', form.errors)
