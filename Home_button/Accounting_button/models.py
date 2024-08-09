
# Create your models here.
# models.py# models.py
from django.db import models
from django.contrib.auth.models import User

class Functions_of_performers(models.Model):
    # Поле name для хранения названия функции исполнителя
    name = models.CharField(max_length=100)
    
    # Поле description для хранения описания функции исполнителя
    description = models.TextField()
    
    # Поле owner для хранения ссылки на пользователя, которому принадлежит функция
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='functions_of_performers')

    def __str__(self):
        # Метод __str__ возвращает название функции исполнителя
        return self.name


class PerformersRates(models.Model):
    name = models.CharField(max_length=100)
    cost_per_minute = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='performers_rates')

    def __str__(self):
        return self.name


from django.db import models
from django.contrib.auth.models import User

class StaffingSchedule(models.Model):
    """
    Модель для хранения расписания штатного расписания.
    """
    # Поле 'name' с выбором из поля 'name' модели 'Functions_of_performers', поведение PROTECT, уникальное значение
    name = models.OneToOneField('Functions_of_performers', on_delete=models.PROTECT)

    # Поле 'rate' с выбором из поля 'name' модели 'PerformersRates', поведение PROTECT
    rate = models.ForeignKey('PerformersRates', on_delete=models.PROTECT)

    # Поле 'quantity' для хранения положительного целого числа
    quantity = models.PositiveIntegerField()

    # Поле 'time_norm' для хранения положительного целого числа
    time_norm = models.PositiveIntegerField()

    # Поле 'time_fund' рассчитывается как произведение 'quantity' и 'time_norm'
    time_fund = models.PositiveIntegerField(editable=False)

    # Поле 'wage_fund' рассчитывается как произведение 'time_fund' и 'cost_per_minute' из 'PerformersRates'
    wage_fund = models.DecimalField(max_digits=15, decimal_places=2, editable=False)

    # Поле 'owner' с поведением SET_NULL, если пользователь удаляется
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='staffing_schedules')

    def save(self, *args, **kwargs):
        # Рассчитываем 'time_fund' как произведение 'quantity' и 'time_norm'
        self.time_fund = self.quantity * self.time_norm

        # Получаем 'cost_per_minute' из связанного 'rate'
        cost_per_minute = self.rate.cost_per_minute

        # Рассчитываем 'wage_fund' как произведение 'time_fund' и 'cost_per_minute'
        self.wage_fund = self.time_fund * cost_per_minute

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


from django.db import models
from django.contrib.auth.models import User

class Functions_of_organizers(models.Model):
    """
    Модель для хранения функций организаторов.
    """
    name = models.CharField(max_length=255)  # Поле для хранения названия функции
    description = models.TextField()  # Поле для хранения описания функции
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='functions_of_organizers')  # Внешний ключ на пользователя, который может быть NULL

    def __str__(self):
        return self.name  # Возвращает название функции при преобразовании объекта в строку



from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class OrganizersRates(models.Model):
    """
    Модель для хранения ставок организаторов.
    """
    name = models.ForeignKey('Functions_of_organizers', on_delete=models.PROTECT)
    # Поле 'name' с выбором из поля 'name' модели 'Functions_of_organizers', поведение PROTECT

    standard = models.DecimalField(max_digits=5, decimal_places=2, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    # Поле 'standard' для хранения положительного числа с двумя знаками после запятой, максимальное значение 100

    description = models.TextField()
    # Поле 'description' для хранения текста

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organizers_rates')
    # Поле 'owner' с поведением SET_NULL, если пользователь удаляется

    def __str__(self):
        return str(self.name)
    # Возвращает название функции при преобразовании объекта в строку


# models.py

from django.db import models
from django.contrib.auth.models import User

class TaxationSystems(models.Model):
    """
    Модель для хранения налоговых систем.
    """
    name = models.CharField(max_length=255)  # Поле для хранения названия налоговой системы
    description = models.TextField()  # Поле для хранения описания налоговой системы
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='taxation_systems')  # Внешний ключ на пользователя, который может быть NULL

    def __str__(self):
        return self.name  # Возвращает название налоговой системы при преобразовании объекта в строку


# models.py

from django.db import models
from django.contrib.auth.models import User

class GroupsOfTypesOfWork(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='groups_of_types_of_work')

    def __str__(self):
        return self.name




from django.db import models
from django.contrib.auth.models import User
from .models import PerformersRates, GroupsOfTypesOfWork  # Импортируем модели PerformersRates и GroupsOfTypesOfWork

# Определяем модель TypesOfJobs
class TypesOfJobs(models.Model):
    name = models.CharField(max_length=255)  # Текстовое поле для названия типа работы
    description = models.TextField()  # Текстовое поле для описания типа работы
    time_standard = models.PositiveIntegerField()  # Положительное целое число для стандарта времени

    # Внешний ключ, связывающийся с полем name модели PerformersRates, с поведением PROTECT
    tariff_name = models.ForeignKey(PerformersRates, on_delete=models.PROTECT, related_name='tariff_names')

    # Внешний ключ, связывающийся с полем name модели GroupsOfTypesOfWork, с поведением PROTECT
    group = models.ForeignKey(GroupsOfTypesOfWork, on_delete=models.PROTECT, related_name='types_of_jobs')

    # Внешний ключ, связывающийся с моделью User, с поведением SET_NULL, измененное значение related_name для избежания конфликта
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='types_of_jobs_owners')

    @property
    def tariff(self):
        return self.tariff_name.cost_per_minute  # Автоматически подставляет значение из поля cost_per_minute модели PerformersRates

    def save(self, *args, **kwargs):
        if not self.owner:
            self.owner = kwargs.pop('owner', None)
        super(TypesOfJobs, self).save(*args, **kwargs)  # Сохраняем объект

    def __str__(self):
        return self.name  # Строковое представление модели


from django.db import models
from django.contrib.auth.models import User

class Clients(models.Model):
    """
    Модель для хранения информации о клиентах.
    """
    short_title = models.CharField(max_length=255)  # Краткое название
    full_name = models.TextField()  # Полное название
    contract_price = models.PositiveIntegerField()  # Стоимость контракта
    inn = models.CharField(max_length=12)  # ИНН
    contract_number_and_date = models.CharField(max_length=255)  # Номер и дата контракта
    tax_system = models.ForeignKey(TaxationSystems, on_delete=models.PROTECT, related_name='clients')  # Налоговая система
    activities = models.TextField()  # Деятельность
    number_of_nomenclature_groups = models.PositiveIntegerField()  # Количество номенклатурных групп
    contact_person = models.CharField(max_length=255)  # Контактное лицо
    telephone = models.CharField(max_length=20)  # Телефон
    email = models.EmailField()  # Адрес электронной почты
    mailing_address = models.TextField()  # Почтовый адрес
    hide_in_search = models.BooleanField(default=False)  # Скрыть в поиске
    comments = models.TextField(blank=True, null=True)  # Комментарии
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='clients')  # Владелец

    def save(self, *args, **kwargs):
        if not self.owner and 'owner' in kwargs:
            self.owner = kwargs.pop('owner')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.short_title  # Возвращает краткое название при преобразовании объекта в строку


# models.py

# models.py
from django.db import models
from django.contrib.auth.models import User

class StandardOperationsLog(models.Model):
    """
    Модель для хранения стандартных операций.
    """
    client = models.ForeignKey('Clients', on_delete=models.PROTECT, related_name='operations_logs')  # Выбор клиента
    type_of_work = models.ForeignKey('TypesOfJobs', on_delete=models.PROTECT, related_name='operations_logs')  # Тип работы
    time_standard = models.PositiveIntegerField()  # Норма времени
    rate = models.DecimalField(max_digits=10, decimal_places=2)  # Тариф
    quantity = models.PositiveIntegerField()  # Количество
    all_the_time = models.PositiveIntegerField()  # Общее время
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена
    date = models.DateTimeField(auto_now_add=True)  # Дата и время записи
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='operations_logs')  # Владелец

    def save(self, *args, **kwargs):
        # Получаем значение time_standard и rate из связанных моделей
        if self.type_of_work:
            self.time_standard = self.type_of_work.time_standard
            self.rate = self.type_of_work.tariff

        # Вычисляем общее время и цену
        self.all_the_time = self.quantity * self.time_standard
        self.price = self.all_the_time * self.rate

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Operation {self.id} - {self.client.short_title}"

    class Meta:
        indexes = [
            models.Index(fields=['owner'], name='idx_owner'),
            models.Index(fields=['client'], name='idx_client'),
            models.Index(fields=['type_of_work'], name='idx_type_of_work'),
        ]




from django.db import models
from django.contrib.auth.models import User

class NonStandardOperationsLog(models.Model):
    """
    Модель для хранения информации о нестандартных операциях.
    """
    client = models.ForeignKey('Clients', on_delete=models.PROTECT, related_name='non_standard_operations_logs')
    content_of_the_work = models.TextField()
    duration = models.PositiveIntegerField()
    rate = models.ForeignKey('PerformersRates', on_delete=models.PROTECT, related_name='non_standard_operations_logs')
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='non_standard_operations_logs')

    class Meta:
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['client']),
        ]

    def save(self, *args, **kwargs):
        # Вычисляем цену как произведение продолжительности и тарифа
        self.price = self.duration * self.rate.cost_per_minute
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.short_title} - {self.content_of_the_work}"



from django.db import models
from django.contrib.auth.models import User

class TypesOfIncome(models.Model):
    """
    Модель для хранения типов доходов.
    """
    name = models.CharField(max_length=255)  # Название
    description = models.TextField()  # Описание
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='types_of_income')  # Владелец

    def save(self, *args, **kwargs):
        if not self.owner and 'owner' in kwargs:
            self.owner = kwargs.pop('owner')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # Возвращает название при преобразовании объекта в строку



from django.db import models
from django.contrib.auth.models import User

class TypesOfExpenses(models.Model):
    """
    Модель для хранения типов расходов.
    """
    name = models.CharField(max_length=255)  # Название
    description = models.TextField()  # Описание
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='types_of_expenses')  # Владелец

    def save(self, *args, **kwargs):
        if not self.owner and 'owner' in kwargs:
            self.owner = kwargs.pop('owner')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # Возвращает название при преобразовании объекта в строку



class IncomeJournal(models.Model):
    name = models.ForeignKey('TypesOfIncome', on_delete=models.PROTECT, related_name='income_journals')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey('Clients', on_delete=models.PROTECT, related_name='income_journals', blank=True, null=True)
    date_of_event = models.DateField()
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='income_journals')

    class Meta:
        indexes = [
            models.Index(fields=['date_of_event']),
            models.Index(fields=['client']),
        ]

    def __str__(self):
        return f"{self.name} - {self.client} - {self.value}"
