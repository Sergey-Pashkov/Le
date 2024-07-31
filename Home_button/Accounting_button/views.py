# Файл: Accounting_button/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

# Представление для дашборда собственника
@login_required
def owner_dashboard(request):
    return render(request, 'Accounting_button/dashboards/owner_dashboard.html')

# Представление для дашборда организатора
@login_required
def organizer_dashboard(request):
    return render(request, 'Accounting_button/dashboards/organizer_dashboard.html')

# Представление для дашборда исполнителя
@login_required
def executor_dashboard(request):
    return render(request, 'Accounting_button/dashboards/executor_dashboard.html')

# Представление для входа
class CustomLoginView(LoginView):
    template_name = 'Accounting_button/login.html'

# Представление для выхода
class CustomLogoutView(LogoutView):
    template_name = 'Accounting_button/logout.html'

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Functions_of_performers
from .forms import FunctionsOfPerformersForm

@login_required
@permission_required('Accounting_button.add_functions_of_performers', raise_exception=True)
def create_function(request):
    """
    Представление для создания новой функции исполнителя.
    Доступно только авторизованным пользователям с правом добавления функций исполнителей.
    """
    if request.method == 'POST':
        form = FunctionsOfPerformersForm(request.POST)
        if form.is_valid():
            function = form.save(commit=False)
            function.owner = request.user  # Устанавливаем текущего пользователя как владельца
            function.save()
            return redirect('Accounting_button:functions_list')
    else:
        form = FunctionsOfPerformersForm()
    return render(request, 'Accounting_button/functions_of_performers/function_form.html', {'form': form})

@login_required
@permission_required('Accounting_button.view_functions_of_performers', raise_exception=True)
def read_function(request, function_id):
    """
    Представление для отображения деталей функции исполнителя.
    Доступно только авторизованным пользователям с правом просмотра функций исполнителей.
    """
    function = get_object_or_404(Functions_of_performers, id=function_id)
    return render(request, 'Accounting_button/functions_of_performers/function_detail.html', {'function': function})

@login_required
@permission_required('Accounting_button.change_functions_of_performers', raise_exception=True)
def update_function(request, function_id):
    """
    Представление для обновления существующей функции исполнителя.
    Доступно только авторизованным пользователям с правом изменения функций исполнителей.
    """
    function = get_object_or_404(Functions_of_performers, id=function_id)
    if request.method == 'POST':
        form = FunctionsOfPerformersForm(request.POST, instance=function)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:functions_list')
    else:
        form = FunctionsOfPerformersForm(instance=function)
    return render(request, 'Accounting_button/functions_of_performers/function_form.html', {'form': form, 'function': function})

@login_required
@permission_required('Accounting_button.delete_functions_of_performers', raise_exception=True)
def delete_function(request, function_id):
    """
    Представление для удаления существующей функции исполнителя.
    Доступно только авторизованным пользователям с правом удаления функций исполнителей.
    """
    function = get_object_or_404(Functions_of_performers, id=function_id)
    if request.method == 'POST':
        function.delete()
        return redirect('Accounting_button:functions_list')
    return render(request, 'Accounting_button/functions_of_performers/function_confirm_delete.html', {'function': function})

@login_required
@permission_required('Accounting_button.view_functions_of_performers', raise_exception=True)
def functions_list(request):
    """
    Представление для отображения списка всех функций исполнителей.
    Доступно только авторизованным пользователям с правом просмотра функций исполнителей.
    """
    functions = Functions_of_performers.objects.all()
    return render(request, 'Accounting_button/functions_of_performers/functions_list.html', {'functions': functions})
