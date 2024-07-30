# Импортируем необходимые модули и функции
from django.urls import path
from . import views

# Определяем пространство имен для URL
app_name = 'Accounting_button'

# Accounting_button/urls.py

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
]
