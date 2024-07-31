
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
