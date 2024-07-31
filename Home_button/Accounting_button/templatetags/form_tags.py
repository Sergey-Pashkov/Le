# templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Добавляет класс к виджету формы.
    
    :param value: Поле формы
    :param arg: Имя класса для добавления
    :return: Поле формы с добавленным классом
    """
    return value.as_widget(attrs={'class': arg})
