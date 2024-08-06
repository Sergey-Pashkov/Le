from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Functions_of_performers

@admin.register(Functions_of_performers)
class FunctionsOfPerformersAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner')
    search_fields = ('name', 'description', 'owner__username')
    list_filter = ('owner',)

# Альтернативный способ регистрации модели
# admin.site.register(Functions_of_performers, FunctionsOfPerformersAdmin)
from django.contrib import admin
from .models import PerformersRates

admin.site.register(PerformersRates)


from .models import StaffingSchedule

admin.site.register(StaffingSchedule)

from django.contrib import admin
from .models import Functions_of_organizers

@admin.register(Functions_of_organizers)
class Functions_of_organizersAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для модели Functions_of_organizers.
    """
    list_display = ('name', 'description', 'owner')  # Поля, отображаемые в списке объектов
    search_fields = ('name', 'description')  # Поля для поиска



from django.contrib import admin
from .models import OrganizersRates

@admin.register(OrganizersRates)
class OrganizersRatesAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для модели OrganizersRates.
    """
    list_display = ('name', 'standard', 'description', 'owner')  # Поля, отображаемые в списке объектов
    search_fields = ('name__name', 'description')  # Поля для поиска


# admin.py

from django.contrib import admin
from .models import TaxationSystems

@admin.register(TaxationSystems)
class TaxationSystemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner')
    search_fields = ('name', 'description')


# admin.py

from django.contrib import admin
from .models import GroupsOfTypesOfWork

@admin.register(GroupsOfTypesOfWork)
class GroupsOfTypesOfWorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner')
    search_fields = ('name', 'description')
