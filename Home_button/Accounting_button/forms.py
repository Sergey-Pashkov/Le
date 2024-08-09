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


from django import forms
from .models import IncomeJournal

class IncomeJournalForm(forms.ModelForm):
    class Meta:
        model = IncomeJournal
        fields = ['name', 'value', 'client', 'date_of_event', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].widget.attrs.update({'disabled': 'true'})  # Отключаем поле client по умолчанию

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        client = cleaned_data.get('client')

        if name and name.name == 'Займы':
            cleaned_data['client'] = None  # Очищаем поле client, если выбрано "Займы"
        elif not client and name and name.name != 'Займы':
            raise forms.ValidationError("Поле 'Клиент' обязательно для заполнения, если не выбран 'Займы'.")
        
        return cleaned_data
