
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



# Пути, относящиеся к модели TaxationSystems

    # Путь для просмотра списка налоговых систем
    path('taxation_systems/', views.taxation_systems_list, name='taxation_systems_list'),
    # Путь для создания новой налоговой системы
    path('taxation_systems/create/', views.create_taxation_system, name='create_taxation_system'),
    # Путь для просмотра деталей налоговой системы по ID
    path('taxation_systems/<int:taxation_system_id>/', views.read_taxation_system, name='read_taxation_system'),
    # Путь для обновления существующей налоговой системы по ID
    path('taxation_systems/<int:taxation_system_id>/update/', views.update_taxation_system, name='update_taxation_system'),
    # Путь для удаления существующей налоговой системы по ID
    path('taxation_systems/<int:taxation_system_id>/delete/', views.delete_taxation_system, name='delete_taxation_system'),

# URL-паттерны для модели GroupsOfTypesOfWork

    path('groups/', views.groups_list, name='groups_list'),  # Путь для списка групп типов работ
    path('groups/create/', views.create_group, name='create_group'),  # Путь для создания новой группы
    path('groups/<int:group_id>/', views.read_group, name='read_group'),  # Путь для чтения группы
    path('groups/<int:group_id>/update/', views.update_group, name='update_group'),  # Путь для обновления группы
    path('groups/<int:group_id>/delete/', views.delete_group, name='delete_group'),  # Путь для удаления группы

    # Путь для списка типов работ
    path('types_of_jobs/', views.types_of_jobs_list, name='types_of_jobs_list'),
    # Путь для создания нового типа работы
    path('types_of_jobs/create/', views.create_type_of_job, name='create_type_of_job'),
    # Путь для просмотра деталей типа работы по ID
    path('types_of_jobs/<int:type_of_job_id>/', views.read_type_of_job, name='read_type_of_job'),
    # Путь для обновления существующего типа работы по ID
    path('types_of_jobs/<int:type_of_job_id>/update/', views.update_type_of_job, name='update_type_of_job'),
    # Путь для удаления существующего типа работы по ID
    path('types_of_jobs/<int:type_of_job_id>/delete/', views.delete_type_of_job, name='delete_type_of_job'),


    # Пути для тарифов исполнителей
    path('rates/', views.rates_list, name='rates_list'),
    path('rates/create/', views.create_performers_rate, name='create_performers_rate'),
    path('rates/<int:rate_id>/', views.read_performers_rate, name='read_performers_rate'),
    path('rates/<int:rate_id>/update/', views.update_performers_rate, name='update_performers_rate'),
    path('rates/<int:rate_id>/delete/', views.delete_performers_rate, name='delete_performers_rate'),

    # Пути для ставок организаторов
    path('organizers_rates/', views.organizers_rates_list, name='organizers_rates_list'),
    path('organizers_rates/create/', views.create_organizers_rate, name='create_organizers_rate'),
    path('organizers_rates/<int:rate_id>/', views.read_organizers_rate, name='read_organizers_rate'),
    path('organizers_rates/<int:rate_id>/update/', views.update_organizers_rate, name='update_organizers_rate'),
    path('organizers_rates/<int:rate_id>/delete/', views.delete_organizers_rate, name='delete_organizers_rate'),

    # выгрузка справочника видов работ
    path('types_of_jobs/export/', views.export_types_of_jobs_to_excel, name='export_types_of_jobs_to_excel'),

    # Путь для списка клиентов
    path('clients/', views.clients_list, name='clients_list'),
    # Путь для создания нового клиента
    path('clients/create/', views.create_client, name='create_client'),
    # Путь для просмотра деталей клиента по ID
    path('clients/<int:client_id>/', views.read_client, name='read_client'),
    # Путь для обновления существующего клиента по ID
    path('clients/<int:client_id>/update/', views.update_client, name='update_client'),
    # Путь для удаления существующего клиента по ID
    path('clients/<int:client_id>/delete/', views.delete_client, name='delete_client'),
    # Путь для экспорта клиентов в Excel
    path('clients/export/', views.export_clients_to_excel, name='export_clients_to_excel'),

    # Пути для стандартных операций
    path('standard_operations_log/', views.standard_operations_log_list, name='standard_operations_log_list'),
    path('standard_operations_log/create/', views.create_standard_operations_log, name='create_standard_operations_log'),
    path('standard_operations_log/<int:log_id>/', views.read_standard_operations_log, name='read_standard_operations_log'),
    path('standard_operations_log/<int:log_id>/update/', views.update_standard_operations_log, name='update_standard_operations_log'),
    path('standard_operations_log/<int:log_id>/delete/', views.delete_standard_operations_log, name='delete_standard_operations_log'),

    # Путь для списка нестандартных операций
    path('non_standard_operations_log/', views.non_standard_operations_log_list, name='non_standard_operations_log_list'),
    # Путь для создания новой записи
    path('non_standard_operations_log/create/', views.create_non_standard_operations_log, name='create_non_standard_operations_log'),
    # Путь для чтения записи
    path('non_standard_operations_log/<int:log_id>/', views.read_non_standard_operations_log, name='read_non_standard_operations_log'),
    # Путь для обновления записи
    path('non_standard_operations_log/<int:log_id>/update/', views.update_non_standard_operations_log, name='update_non_standard_operations_log'),
    # Путь для удаления записи
    path('non_standard_operations_log/<int:log_id>/delete/', views.delete_non_standard_operations_log, name='delete_non_standard_operations_log'),
]
