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
