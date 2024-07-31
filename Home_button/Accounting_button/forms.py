from django import forms
from .models import Functions_of_performers

class FunctionsOfPerformersForm(forms.ModelForm):
    class Meta:
        model = Functions_of_performers
        fields = ['name', 'description']  # Убираем поле 'owner'


# Accounting_button/forms.py
from django import forms
from .models import PerformersRates  # Импортируем модель

# Форма для создания и редактирования тарифов исполнителей
class PerformersRatesForm(forms.ModelForm):
    class Meta:
        model = PerformersRates  # Указываем модель для формы
        fields = ['name', 'cost_per_minute']  # Поля, которые будут использоваться в форме
