# Accounting_button/tests/test_templatetags.py
from django import forms
from django.template import Context, Template
from django.test import SimpleTestCase
from Accounting_button.templatetags.form_tags import add_class

class TestAddClassFilter(SimpleTestCase):

    def test_add_class_filter(self):
        """
        Проверяет, что фильтр add_class добавляет указанный класс к виджету формы.
        """
        # Создаем простую форму для теста
        class TestForm(forms.Form):
            name = forms.CharField()

        # Создаем экземпляр формы
        form = TestForm()
        
        # Применяем фильтр add_class к полю формы
        rendered = add_class(form['name'], 'test-class')
        
        # Проверяем, что виджет формы содержит указанный класс
        self.assertIn('class="test-class"', str(rendered))

    def test_add_class_in_template(self):
        """
        Проверяет, что фильтр add_class работает корректно в шаблоне.
        """
        # Создаем простую форму для теста
        class TestForm(forms.Form):
            name = forms.CharField()

        # Создаем экземпляр формы
        form = TestForm()
        
        # Создаем тестовый шаблон, который использует фильтр add_class
        template = Template("{% load form_tags %}{{ form.name|add_class:'test-class' }}")
        
        # Рендерим шаблон с контекстом, содержащим форму
        context = Context({'form': form})
        rendered = template.render(context)
        
        # Проверяем, что виджет формы содержит указанный класс
        self.assertIn('class="test-class"', rendered)
