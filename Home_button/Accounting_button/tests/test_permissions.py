# Accounting_button/tests/test_permissions.py

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from Accounting_button.templatetags.permissions import has_group, has_perm

class TestPermissionsFilters(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='password')

        # Создаем группу и добавляем пользователя в группу
        self.group = Group.objects.create(name='testgroup')
        self.user.groups.add(self.group)

        # Создаем разрешение и добавляем его к пользователю
        content_type = ContentType.objects.get_for_model(User)
        self.permission = Permission.objects.create(
            codename='test_permission',
            name='Test Permission',
            content_type=content_type
        )
        self.user.user_permissions.add(self.permission)

    def test_has_group(self):
        """
        Проверяет, что фильтр has_group правильно определяет принадлежность пользователя к группе.
        """
        self.assertTrue(has_group(self.user, 'testgroup'))
        self.assertFalse(has_group(self.user, 'nonexistentgroup'))

    def test_has_perm(self):
        """
        Проверяет, что фильтр has_perm правильно определяет наличие у пользователя разрешения.
        """
        # Используем полный путь к разрешению
        permission_name = f'{self.permission.content_type.app_label}.test_permission'
        self.assertTrue(has_perm(self.user, permission_name))
        self.assertFalse(has_perm(self.user, 'nonexistent_permission'))
