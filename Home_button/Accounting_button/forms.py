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


# forms.py
from django import forms
from .models import TaxationSystems

class TaxationSystemsForm(forms.ModelForm):
    class Meta:
        model = TaxationSystems
        fields = ['name', 'description']


from django import forms
from .models import GroupsOfTypesOfWork

class GroupsOfTypesOfWorkForm(forms.ModelForm):
    class Meta:
        model = GroupsOfTypesOfWork
        fields = ['name', 'description']

from django import forms
from .models import TypesOfJobs

class TypesOfJobsForm(forms.ModelForm):
    class Meta:
        model = TypesOfJobs
        fields = ['name', 'description', 'time_standard', 'tariff_name', 'group']



from django import forms
from .models import Clients

class ClientsForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['short_title', 'full_name', 'contract_price', 'inn', 'contract_number_and_date',
                  'tax_system', 'activities', 'number_of_nomenclature_groups', 'contact_person',
                  'telephone', 'email', 'mailing_address', 'hide_in_search', 'comments']

    hide_in_search = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)




# forms.py
from django import forms
from .models import StandardOperationsLog

class StandardOperationsLogForm(forms.ModelForm):
    """
    Форма для модели StandardOperationsLog.
    """

    class Meta:
        model = StandardOperationsLog
        fields = ['client', 'type_of_work', 'quantity']  # Указываем только те поля, которые должны быть доступны в форме

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Получаем request из kwargs
        super(StandardOperationsLogForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(StandardOperationsLogForm, self).save(commit=False)
        if self.request and not instance.owner:
            instance.owner = self.request.user  # Устанавливаем владельца, если он не задан
        if commit:
            instance.save()
        return instance







from django import forms
from .models import NonStandardOperationsLog

class NonStandardOperationsLogForm(forms.ModelForm):
    """
    Форма для модели NonStandardOperationsLog.
    """

    class Meta:
        model = NonStandardOperationsLog
        fields = ['client', 'content_of_the_work', 'duration', 'rate']  # Указываем только те поля, которые должны быть доступны в форме

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Получаем request из kwargs
        super(NonStandardOperationsLogForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(NonStandardOperationsLogForm, self).save(commit=False)
        if self.request and not instance.owner_id:
            instance.owner = self.request.user  # Устанавливаем владельца, если он не задан
        if commit:
            instance.save()
        return instance



from django import forms
from .models import TypesOfIncome

class TypesOfIncomeForm(forms.ModelForm):
    """
    Форма для модели TypesOfIncome.
    """

    class Meta:
        model = TypesOfIncome
        fields = ['name', 'description']  # Указываем только те поля, которые должны быть доступны в форме


from django import forms
from .models import TypesOfExpenses

class TypesOfExpensesForm(forms.ModelForm):
    """
    Форма для модели TypesOfExpenses.
    """

    class Meta:
        model = TypesOfExpenses
        fields = ['name', 'description']  # Убираем поле 'owner'




# Журнал доходов
from django import forms
from .models import IncomeJournal
from django.utils import timezone
from datetime import timedelta
import calendar

class IncomeJournalForm(forms.ModelForm):
    class Meta:
        model = IncomeJournal
        fields = ['name', 'value', 'client', 'date_of_event', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Установка даты предыдущего рабочего дня по умолчанию
        self.fields['date_of_event'].initial = self.get_previous_working_day()

        # Обновление состояния поля client
        self.update_client_field_state()

    def get_previous_working_day(self):
        """
        Возвращает предыдущий рабочий день.
        """
        today = timezone.now().date()
        previous_day = today - timedelta(days=1)
        
        # Если предыдущий день — это суббота или воскресенье, переместитесь к пятнице
        if previous_day.weekday() == 5:  # Суббота
            previous_day -= timedelta(days=1)
        elif previous_day.weekday() == 6:  # Воскресенье
            previous_day -= timedelta(days=2)
        
        return previous_day

    def update_client_field_state(self):
        """
        Очищает и отключает поле client, если выбран тип дохода 'Займы'.
        """
        name = self.initial.get('name') or self.data.get('name')
        if name:
            name_instance = self.fields['name'].queryset.get(pk=name)
            if name_instance.name == 'Займы':
                self.fields['client'].widget.attrs.update({'disabled': 'true'})
                self.initial['client'] = None

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        client = cleaned_data.get('client')

        if name and name.name == 'Займы':
            cleaned_data['client'] = None  # Очищаем поле client для "Займы"
        
        if cleaned_data.get('client') is None and name.name != 'Займы':
            self.add_error('client', "Поле 'Клиент' не может быть пустым.")
        
        return cleaned_data


#журнал расходов
from django import forms
from .models import ExpenseJournal
from django.utils import timezone
from datetime import timedelta

class ExpenseJournalForm(forms.ModelForm):
    class Meta:
        model = ExpenseJournal
        fields = ['name', 'value', 'date_of_event', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_event'].initial = self.get_previous_working_day()

    def get_previous_working_day(self):
        """ Возвращает предыдущий рабочий день. """
        today = timezone.now().date()
        previous_day = today - timedelta(days=1)
        
        while previous_day.weekday() > 4:  # Если суббота или воскресенье
            previous_day -= timedelta(days=1)
        
        return previous_day




from django import forms
from .models import RevenueBudget

class RevenueBudgetForm(forms.ModelForm):
    class Meta:
        model = RevenueBudget
        fields = ['name', 'value', 'period', 'comment']
        widgets = {
            'period': forms.DateInput(attrs={'type': 'month'}, format='%Y-%m'),
        }

    def clean_period(self):
        period = self.cleaned_data.get('period')
        # Если period уже строка (например, 'YYYY-MM'), просто возвращаем её
        if isinstance(period, str):
            return period
        # Если период был передан как объект даты (должно быть очень редко),
        # преобразуем его в строку 'YYYY-MM'
        if period:
            return period.strftime('%Y-%m')
        return period
