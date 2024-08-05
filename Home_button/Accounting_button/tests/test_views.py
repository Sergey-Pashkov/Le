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


# Accounting_button/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission, ContentType
from Accounting_button.models import PerformersRates
from Accounting_button.forms import PerformersRatesForm

class PerformersRatesViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        content_type = ContentType.objects.get_for_model(PerformersRates)
        self.add_permission = Permission.objects.get(codename='add_performersrates', content_type=content_type)
        self.view_permission = Permission.objects.get(codename='view_performersrates', content_type=content_type)
        self.change_permission = Permission.objects.get(codename='change_performersrates', content_type=content_type)
        self.delete_permission = Permission.objects.get(codename='delete_performersrates', content_type=content_type)
        self.user.user_permissions.add(self.add_permission, self.view_permission, self.change_permission, self.delete_permission)
        self.client.login(username='testuser', password='testpassword')
        self.rate = PerformersRates.objects.create(name='Rate 1', cost_per_minute=1.5, owner=self.user)

    def test_create_rate(self):
        response = self.client.post(reverse('Accounting_button:create_rate'), {
            'name': 'Rate 2',
            'cost_per_minute': 2.5,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PerformersRates.objects.count(), 2)

    def test_read_rate(self):
        response = self.client.get(reverse('Accounting_button:read_rate', args=[self.rate.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rate 1')

    def test_update_rate(self):
        response = self.client.post(reverse('Accounting_button:update_rate', args=[self.rate.id]), {
            'name': 'Rate 1 updated',
            'cost_per_minute': 2.0,
        })
        self.assertEqual(response.status_code, 302)
        self.rate.refresh_from_db()
        self.assertEqual(self.rate.name, 'Rate 1 updated')

    def test_delete_rate(self):
        response = self.client.post(reverse('Accounting_button:delete_rate', args=[self.rate.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PerformersRates.objects.count(), 0)





from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from Accounting_button.models import Functions_of_performers, PerformersRates, StaffingSchedule
from Accounting_button.forms import StaffingScheduleForm

class StaffingScheduleViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Создаем пользователя и даем ему необходимые разрешения
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.user_permissions.add(Permission.objects.get(codename='view_staffingschedule'))
        self.user.user_permissions.add(Permission.objects.get(codename='add_staffingschedule'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_staffingschedule'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_staffingschedule'))
        self.client.login(username='testuser', password='12345')

        # Создаем данные для тестирования
        self.function = Functions_of_performers.objects.create(name='Function1')
        self.function2 = Functions_of_performers.objects.create(name='Function2')
        self.rate = PerformersRates.objects.create(name='Rate1', cost_per_minute=2.5)
        self.schedule = StaffingSchedule.objects.create(
            name=self.function,
            rate=self.rate,
            quantity=10,
            time_norm=60,
            owner=self.user
        )

    def test_schedules_list_view(self):
        response = self.client.get(reverse('Accounting_button:schedules_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/staffing_schedule/schedule_list.html')
        self.assertContains(response, self.schedule.name.name)
        self.assertContains(response, self.schedule.rate.name)

    def test_create_schedule_view(self):
        response = self.client.get(reverse('Accounting_button:create_schedule'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/staffing_schedule/schedule_form.html')

        form_data = {
            'name': self.function2.id,  # Используем другое имя, чтобы избежать дублирования
            'rate': self.rate.id,
            'quantity': 20,
            'time_norm': 40
        }
        response = self.client.post(reverse('Accounting_button:create_schedule'), data=form_data)
        if response.status_code == 200:
            print(response.context['form'].errors)  # Вывод ошибок формы, если они есть
        self.assertEqual(response.status_code, 302)  # Проверяем редирект после успешного создания
        self.assertEqual(StaffingSchedule.objects.count(), 2)  # Проверяем, что объект был создан

    def test_read_schedule_view(self):
        response = self.client.get(reverse('Accounting_button:read_schedule', args=[self.schedule.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/staffing_schedule/schedule_detail.html')
        self.assertContains(response, self.schedule.name.name)

    def test_update_schedule_view(self):
        response = self.client.get(reverse('Accounting_button:update_schedule', args=[self.schedule.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/staffing_schedule/schedule_form.html')

        form_data = {
            'name': self.function.id,
            'rate': self.rate.id,
            'quantity': 15,
            'time_norm': 50
        }
        response = self.client.post(reverse('Accounting_button:update_schedule', args=[self.schedule.id]), data=form_data)
        self.assertEqual(response.status_code, 302)  # Проверяем редирект после успешного обновления
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.quantity, 15)
        self.assertEqual(self.schedule.time_norm, 50)

    def test_delete_schedule_view(self):
        response = self.client.get(reverse('Accounting_button:delete_schedule', args=[self.schedule.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/staffing_schedule/schedule_confirm_delete.html')

        response = self.client.post(reverse('Accounting_button:delete_schedule', args=[self.schedule.id]))
        self.assertEqual(response.status_code, 302)  # Проверяем редирект после успешного удаления
        self.assertEqual(StaffingSchedule.objects.count(), 0)  # Проверяем, что объект был удален




from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from Accounting_button.models import Functions_of_performers, PerformersRates, StaffingSchedule
from django.db.models import ProtectedError

class StaffingScheduleViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Создаем пользователя и даем ему необходимые разрешения
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.user_permissions.add(Permission.objects.get(codename='view_staffingschedule'))
        self.user.user_permissions.add(Permission.objects.get(codename='add_staffingschedule'))
        self.user.user_permissions.add(Permission.objects.get(codename='change_staffingschedule'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_staffingschedule'))
        self.user.user_permissions.add(Permission.objects.get(codename='delete_functions_of_performers'))
        self.client.login(username='testuser', password='12345')

        # Создаем данные для тестирования
        self.function = Functions_of_performers.objects.create(name='Function1')
        self.function2 = Functions_of_performers.objects.create(name='Function2')
        self.rate = PerformersRates.objects.create(name='Rate1', cost_per_minute=2.5)
        self.schedule = StaffingSchedule.objects.create(
            name=self.function,
            rate=self.rate,
            quantity=10,
            time_norm=60,
            owner=self.user
        )

    def test_protected_error_on_delete_function(self):
        # Проверка, что при попытке удалить функцию, используемую в StaffingSchedule, возникает ProtectedError
        response = self.client.post(reverse('Accounting_button:delete_function', args=[self.function.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('Accounting_button:functions_list'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Невозможно удалить эту функцию, так как она связана с расписанием штатного расписания.')
        self.assertEqual(messages[0].level, messages[0].ERROR)

    def test_delete_function_view_permission(self):
        # Проверка, что при попытке удаления функции без нужных разрешений возвращается 403
        self.user.user_permissions.remove(Permission.objects.get(codename='delete_functions_of_performers'))
        response = self.client.post(reverse('Accounting_button:delete_function', args=[self.function.id]))
        self.assertEqual(response.status_code, 403)
