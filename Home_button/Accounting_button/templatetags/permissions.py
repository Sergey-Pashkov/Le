# Accounting_button/templatetags/permissions.py

from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Проверяет, принадлежит ли пользователь к определенной группе.
    
    :param user: Пользователь
    :param group_name: Имя группы
    :return: True, если пользователь принадлежит к группе, иначе False
    """
    return user.groups.filter(name=group_name).exists()

@register.filter(name='has_perm')
def has_perm(user, perm_name):
    """
    Проверяет, имеет ли пользователь определенное разрешение.
    
    :param user: Пользователь
    :param perm_name: Имя разрешения
    :return: True, если пользователь имеет разрешение, иначе False
    """
    return user.has_perm(perm_name)
