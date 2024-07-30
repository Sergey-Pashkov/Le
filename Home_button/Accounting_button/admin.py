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
