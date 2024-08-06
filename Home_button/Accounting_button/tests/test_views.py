# Accounting_button/tests/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission, ContentType
from Accounting_button.models import PerformersRates, Functions_of_performers, StaffingSchedule, Functions_of_organizers

class PerformersRatesViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        content_type = ContentType.objects.get_for_model(PerformersRates)
        
        # Добавляем все необходимые разрешения пользователю
        permissions = [
            Permission.objects.get(codename='add_performersrates', content_type=content_type),
            Permission.objects.get(codename='view_performersrates', content_type=content_type),
            Permission.objects.get(codename='change_performersrates', content_type=content_type),
            Permission.objects.get(codename='delete_performersrates', content_type=content_type)
        ]
        
        self.user.user_permissions.add(*permissions)
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

class FunctionsOfPerformersViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        content_type = ContentType.objects.get_for_model(Functions_of_performers)
        
        permissions = [
            Permission.objects.get(codename='add_functions_of_performers', content_type=content_type),
            Permission.objects.get(codename='view_functions_of_performers', content_type=content_type),
            Permission.objects.get(codename='change_functions_of_performers', content_type=content_type),
            Permission.objects.get(codename='delete_functions_of_performers', content_type=content_type)
        ]
        
        self.user.user_permissions.add(*permissions)
        self.client.login(username='testuser', password='testpassword')
        self.function = Functions_of_performers.objects.create(
            name='Test Function',
            description='This is a test function description',
            owner=self.user
        )

    def test_create_function_view(self):
        response = self.client.post(reverse('Accounting_button:create_function'), {
            'name': 'New Function',
            'description': 'New function description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Functions_of_performers.objects.filter(name='New Function').exists())

    def test_read_function_view(self):
        response = self.client.get(reverse('Accounting_button:read_function', args=[self.function.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/functions_of_performers/function_detail.html')
        self.assertContains(response, self.function.name)

    def test_update_function_view(self):
        response = self.client.post(reverse('Accounting_button:update_function', args=[self.function.id]), {
            'name': 'Updated Function',
            'description': 'Updated function description'
        })
        self.assertEqual(response.status_code, 302)
        self.function.refresh_from_db()
        self.assertEqual(self.function.name, 'Updated Function')

    def test_delete_function_view(self):
        response = self.client.post(reverse('Accounting_button:delete_function', args=[self.function.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Functions_of_performers.objects.filter(id=self.function.id).exists())

    def test_functions_list_view(self):
        response = self.client.get(reverse('Accounting_button:functions_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/functions_of_performers/functions_list.html')
        self.assertContains(response, self.function.name)

class StaffingScheduleViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        content_type = ContentType.objects.get_for_model(StaffingSchedule)
        
        permissions = [
            Permission.objects.get(codename='view_staffingschedule', content_type=content_type),
            Permission.objects.get(codename='add_staffingschedule', content_type=content_type),
            Permission.objects.get(codename='change_staffingschedule', content_type=content_type),
            Permission.objects.get(codename='delete_staffingschedule', content_type=content_type)
        ]
        
        self.user.user_permissions.add(*permissions)
        self.client.login(username='testuser', password='testpassword')
        self.function = Functions_of_performers.objects.create(name='Function1')
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
            'name': self.function.id,
            'rate': self.rate.id,
            'quantity': 20,
            'time_norm': 40
        }
        response = self.client.post(reverse('Accounting_button:create_schedule'), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(StaffingSchedule.objects.count(), 2)

    def test_read_schedule_view(self):
        response = self.client.get(reverse('Accounting_button:read_schedule', args=[self.schedule.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/staffing_schedule/schedule_detail.html')
        self.assertContains(response, self.schedule.name.name)

    def test_update_schedule_view(self):
        response = self.client.post(reverse('Accounting_button:update_schedule', args=[self.schedule.id]), {
            'name': self.function.id,
            'rate': self.rate.id,
            'quantity': 15,
            'time_norm': 50
        })
        self.assertEqual(response.status_code, 302)
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.quantity, 15)
        self.assertEqual(self.schedule.time_norm, 50)

    def test_delete_schedule_view(self):
        response = self.client.post(reverse('Accounting_button:delete_schedule', args=[self.schedule.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(StaffingSchedule.objects.count(), 0)

class FunctionsOfOrganizersViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        content_type = ContentType.objects.get_for_model(Functions_of_organizers)
        
        permissions = [
            Permission.objects.get(codename='add_functions_of_organizers', content_type=content_type),
            Permission.objects.get(codename='view_functions_of_organizers', content_type=content_type),
            Permission.objects.get(codename='change_functions_of_organizers', content_type=content_type),
            Permission.objects.get(codename='delete_functions_of_organizers', content_type=content_type)
        ]
        
        self.user.user_permissions.add(*permissions)
        self.client.login(username='testuser', password='testpassword')
        self.function = Functions_of_organizers.objects.create(
            name='Организатор мероприятия',
            description='Отвечает за организацию и проведение мероприятий.',
            owner=self.user
        )

    def test_create_function_organizer_view(self):
        response = self.client.post(reverse('Accounting_button:create_function_organizer'), {
            'name': 'New Organizer',
            'description': 'New function description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Functions_of_organizers.objects.filter(name='New Organizer').exists())

    def test_read_function_organizer_view(self):
        response = self.client.get(reverse('Accounting_button:read_function_organizer', args=[self.function.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/functions_of_organizers/function_detail.html')
        self.assertContains(response, self.function.name)

    def test_update_function_organizer_view(self):
        response = self.client.post(reverse('Accounting_button:update_function_organizer', args=[self.function.id]), {
            'name': 'Updated Organizer',
            'description': 'Updated function description'
        })
        self.assertEqual(response.status_code, 302)
        self.function.refresh_from_db()
        self.assertEqual(self.function.name, 'Updated Organizer')

    def test_delete_function_organizer_view(self):
        response = self.client.post(reverse('Accounting_button:delete_function_organizer', args=[self.function.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Functions_of_organizers.objects.filter(id=self.function.id).exists())

    def test_functions_organizers_list_view(self):
        response = self.client.get(reverse('Accounting_button:functions_organizers_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Accounting_button/functions_of_organizers/functions_list.html')
        self.assertContains(response, self.function.name)

