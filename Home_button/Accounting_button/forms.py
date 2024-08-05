# Accounting_button/forms.py
from django import forms
from .models import Functions_of_performers, PerformersRates
from django.core.exceptions import ValidationError

class FunctionsOfPerformersForm(forms.ModelForm):
    class Meta:
        model = Functions_of_performers
        fields = ['name', 'description']  # Убираем поле 'owner'

class PerformersRatesForm(forms.ModelForm):
    class Meta:
        model = PerformersRates  # Указываем модель для формы
        fields = ['name', 'cost_per_minute']  # Поля, которые будут использоваться в форме

    def clean_cost_per_minute(self):
        cost = self.cleaned_data.get('cost_per_minute')
        if cost < 0:
            raise ValidationError("Стоимость за минуту не может быть отрицательной.")
        return cost



from django import forms
from .models import StaffingSchedule

# Форма для создания и редактирования расписаний штатного расписания
class StaffingScheduleForm(forms.ModelForm):
    class Meta:
        model = StaffingSchedule  # Указываем модель для формы
        fields = ['name', 'rate', 'quantity', 'time_norm']  # Поля, которые будут использоваться в форме

from django import forms
from .models import Functions_of_organizers

class FunctionsOfOrganizersForm(forms.ModelForm):
    class Meta:
        model = Functions_of_organizers
        fields = ['name', 'description']


from django import forms
from .models import OrganizersRates

class OrganizersRatesForm(forms.ModelForm):
    class Meta:
        model = OrganizersRates
        fields = ['name', 'standard', 'description']
