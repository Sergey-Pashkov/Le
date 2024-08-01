
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



class StaffingSchedule(models.Model):
    # Поле 'name' с выбором из поля 'name' модели 'Functions_of_performers', поведение PROTECT, уникальное значение
    name = models.ForeignKey('Functions_of_performers', on_delete=models.PROTECT, unique=True)

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
