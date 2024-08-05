
# Accounting_button/urls.py
from django.urls import path
from . import views

# Определяем пространство имен для URL
app_name = 'Accounting_button'

urlpatterns = [
    path('dashboard/owner/', views.owner_dashboard, name='owner_dashboard'),
    path('dashboard/organizer/', views.organizer_dashboard, name='organizer_dashboard'),
    path('dashboard/executor/', views.executor_dashboard, name='executor_dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Путь для кастомного входа
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    path('functions/', views.functions_list, name='functions_list'),
    path('functions/create/', views.create_function, name='create_function'),
    path('functions/<int:function_id>/', views.read_function, name='read_function'),
    path('functions/<int:function_id>/update/', views.update_function, name='update_function'),
    path('functions/<int:function_id>/delete/', views.delete_function, name='delete_function'),

    path('rates/', views.rates_list, name='rates_list'),  # Путь для списка тарифов
    path('rates/create/', views.create_rate, name='create_rate'),  # Путь для создания тарифа
    path('rates/<int:rate_id>/', views.read_rate, name='read_rate'),  # Путь для отображения деталей тарифа
    path('rates/<int:rate_id>/update/', views.update_rate, name='update_rate'),  # Путь для обновления тарифа
    path('rates/<int:rate_id>/delete/', views.delete_rate, name='delete_rate'),  # Путь для удаления тарифа

    # Пути для управления расписаниями штата
    path('schedules/', views.schedules_list, name='schedules_list'),  # Путь для просмотра списка расписаний
    path('schedules/create/', views.create_schedule, name='create_schedule'),  # Путь для создания нового расписания
    path('schedules/<int:schedule_id>/', views.read_schedule, name='read_schedule'),  # Путь для просмотра деталей расписания
    path('schedules/<int:schedule_id>/update/', views.update_schedule, name='update_schedule'),  # Путь для обновления расписания
    path('schedules/<int:schedule_id>/delete/', views.delete_schedule, name='delete_schedule'),  # Путь для удаления расписания

    # Путь для отображения списка функций организаторов
    path('functions/organizers/', views.functions_organizers_list, name='functions_organizers_list'),
    
    # Путь для создания новой функции организатора
    path('functions/organizers/create/', views.create_function_organizer, name='create_function_organizer'),
    
    # Путь для отображения деталей функции организатора
    path('functions/organizers/<int:function_id>/', views.read_function_organizer, name='read_function_organizer'),
    
    # Путь для обновления существующей функции организатора
    path('functions/organizers/<int:function_id>/update/', views.update_function_organizer, name='update_function_organizer'),
    
    # Путь для удаления существующей функции организатора
    path('functions/organizers/<int:function_id>/delete/', views.delete_function_organizer, name='delete_function_organizer'),
]
