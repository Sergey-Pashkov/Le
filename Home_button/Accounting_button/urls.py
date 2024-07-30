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
]
