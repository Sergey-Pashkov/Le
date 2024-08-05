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
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from .models import Functions_of_performers  

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
    # Получаем объект функции по ID или возвращаем 404, если не найдено
    function = get_object_or_404(Functions_of_performers, id=function_id)
    
    # Если запрос POST, пытаемся удалить функцию
    if request.method == 'POST':
        try:
            # Пытаемся удалить функцию
            function.delete()
            # Добавляем сообщение об успешном удалении
            messages.success(request, 'Функция успешно удалена.')
        except ProtectedError:
            # Если возникает ошибка ProtectedError, добавляем сообщение об ошибке
            messages.error(request, 'Невозможно удалить эту функцию, так как она связана с расписанием штатного расписания.', extra_tags='alert-danger')
        # Редирект на страницу списка функций
        return redirect('Accounting_button:functions_list')
    
    # Если запрос не POST, отображаем страницу подтверждения удаления
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


# Accounting_button/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import PerformersRates
from .forms import PerformersRatesForm

# Представление для создания нового тарифа
@login_required
@permission_required('Accounting_button.add_performersrates', raise_exception=True)
def create_rate(request):
    if request.method == 'POST':
        form = PerformersRatesForm(request.POST)  # Создаем форму с данными из запроса
        if form.is_valid():
            rate = form.save(commit=False)
            rate.owner = request.user  # Устанавливаем текущего пользователя как владельца
            rate.save()  # Сохраняем тариф
            return redirect('Accounting_button:rates_list')  # Перенаправляем на список тарифов
    else:
        form = PerformersRatesForm()  # Пустая форма для GET-запроса
    return render(request, 'Accounting_button/performers_rates/rate_form.html', {'form': form})

# Представление для отображения деталей тарифа
@login_required
@permission_required('Accounting_button.view_performersrates', raise_exception=True)
def read_rate(request, rate_id):
    rate = get_object_or_404(PerformersRates, id=rate_id)  # Получаем тариф или возвращаем 404
    return render(request, 'Accounting_button/performers_rates/rate_detail.html', {'rate': rate})

# Представление для обновления существующего тарифа
@login_required
@permission_required('Accounting_button.change_performersrates', raise_exception=True)
def update_rate(request, rate_id):
    rate = get_object_or_404(PerformersRates, id=rate_id)  # Получаем тариф или возвращаем 404
    if request.method == 'POST':
        form = PerformersRatesForm(request.POST, instance=rate)  # Создаем форму с данными из запроса и экземпляром тарифа
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect('Accounting_button:rates_list')  # Перенаправляем на список тарифов
    else:
        form = PerformersRatesForm(instance=rate)  # Форма с данными тарифа для GET-запроса
    return render(request, 'Accounting_button/performers_rates/rate_form.html', {'form': form, 'rate': rate})

# Представление для удаления существующего тарифа
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from .models import PerformersRates

@login_required
@permission_required('Accounting_button.delete_performersrates', raise_exception=True)
def delete_rate(request, rate_id):
    """
    Представление для удаления существующего тарифа исполнителя.
    Доступно только авторизованным пользователям с правом удаления тарифов исполнителей.
    """
    rate = get_object_or_404(PerformersRates, id=rate_id)
    if request.method == 'POST':
        try:
            rate.delete()
            messages.success(request, 'Тариф успешно удален.')
        except ProtectedError:
            messages.error(request, 'Невозможно удалить этот тариф, так как он связан с расписанием штатного расписания.', extra_tags='alert-danger')
        return redirect('Accounting_button:rates_list')
    return render(request, 'Accounting_button/performers_rates/rate_confirm_delete.html', {'rate': rate})

# Представление для отображения списка всех тарифов исполнителей
@login_required
@permission_required('Accounting_button.view_performersrates', raise_exception=True)
def rates_list(request):
    rates = PerformersRates.objects.all()  # Получаем все тарифы из базы данных
    return render(request, 'Accounting_button/performers_rates/rates_list.html', {'rates': rates})

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Functions_of_performers, PerformersRates, StaffingSchedule
from .forms import FunctionsOfPerformersForm, PerformersRatesForm, StaffingScheduleForm

@login_required
@permission_required('Accounting_button.view_staffingschedule', raise_exception=True)
def schedules_list(request):
    schedules = StaffingSchedule.objects.all()

    total_time_fund = sum(schedule.time_fund for schedule in schedules)
    total_wage_fund = sum(schedule.wage_fund for schedule in schedules)
    total_quantity = sum(schedule.quantity for schedule in schedules)
    total_time_fund_hours = total_time_fund / 60.0

    # Добавим перевод фонда времени для каждого расписания в часы
    for schedule in schedules:
        schedule.time_fund_hours = schedule.time_fund / 60.0

    return render(request, 'Accounting_button/staffing_schedule/schedule_list.html', {
        'schedules': schedules,
        'total_time_fund': total_time_fund,
        'total_wage_fund': total_wage_fund,
        'total_quantity': total_quantity,
        'total_time_fund_hours': total_time_fund_hours,
    })


# Другие представления для создания, чтения, обновления и удаления расписаний
@login_required
@permission_required('Accounting_button.add_staffingschedule', raise_exception=True)
def create_schedule(request):
    """
    Представление для создания нового расписания штата.
    Доступно только авторизованным пользователям с соответствующим разрешением.
    """
    if request.method == 'POST':
        form = StaffingScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.owner = request.user
            schedule.save()
            return redirect('Accounting_button:schedules_list')
    else:
        form = StaffingScheduleForm()
    return render(request, 'Accounting_button/staffing_schedule/schedule_form.html', {'form': form})

@login_required
@permission_required('Accounting_button.view_staffingschedule', raise_exception=True)
def read_schedule(request, schedule_id):
    """
    Представление для отображения деталей расписания штата.
    Доступно только авторизованным пользователям с соответствующим разрешением.
    """
    schedule = get_object_or_404(StaffingSchedule, id=schedule_id)
    return render(request, 'Accounting_button/staffing_schedule/schedule_detail.html', {'schedule': schedule})

@login_required
@permission_required('Accounting_button.change_staffingschedule', raise_exception=True)
def update_schedule(request, schedule_id):
    """
    Представление для обновления существующего расписания штата.
    Доступно только авторизованным пользователям с соответствующим разрешением.
    """
    schedule = get_object_or_404(StaffingSchedule, id=schedule_id)
    if request.method == 'POST':
        form = StaffingScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:schedules_list')
    else:
        form = StaffingScheduleForm(instance=schedule)
    return render(request, 'Accounting_button/staffing_schedule/schedule_form.html', {'form': form, 'schedule': schedule})

@login_required
@permission_required('Accounting_button.delete_staffingschedule', raise_exception=True)
def delete_schedule(request, schedule_id):
    """
    Представление для удаления существующего расписания штата.
    Доступно только авторизованным пользователям с соответствующим разрешением.
    """
    schedule = get_object_or_404(StaffingSchedule, id=schedule_id)
    if request.method == 'POST':
        schedule.delete()
        return redirect('Accounting_button:schedules_list')
    return render(request, 'Accounting_button/staffing_schedule/schedule_confirm_delete.html', {'schedule': schedule})





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Functions_of_organizers
from .forms import FunctionsOfOrganizersForm
from django.contrib import messages
from django.db.models import ProtectedError

@login_required
@permission_required('Accounting_button.add_functions_of_organizers', raise_exception=True)
def create_function_organizer(request):
    """
    Представление для создания новой функции организатора.
    Доступно только авторизованным пользователям с правом добавления функций организаторов.
    """
    if request.method == 'POST':
        form = FunctionsOfOrganizersForm(request.POST)
        if form.is_valid():
            function = form.save(commit=False)
            function.owner = request.user  # Устанавливаем текущего пользователя как владельца
            function.save()
            return redirect('Accounting_button:functions_organizers_list')
    else:
        form = FunctionsOfOrganizersForm()
    return render(request, 'Accounting_button/functions_of_organizers/function_form.html', {'form': form})

@login_required
@permission_required('Accounting_button.view_functions_of_organizers', raise_exception=True)
def read_function_organizer(request, function_id):
    """
    Представление для отображения деталей функции организатора.
    Доступно только авторизованным пользователям с правом просмотра функций организаторов.
    """
    function = get_object_or_404(Functions_of_organizers, id=function_id)
    return render(request, 'Accounting_button/functions_of_organizers/function_detail.html', {'function': function})

@login_required
@permission_required('Accounting_button.change_functions_of_organizers', raise_exception=True)
def update_function_organizer(request, function_id):
    """
    Представление для обновления существующей функции организатора.
    Доступно только авторизованным пользователям с правом изменения функций организаторов.
    """
    function = get_object_or_404(Functions_of_organizers, id=function_id)
    if request.method == 'POST':
        form = FunctionsOfOrganizersForm(request.POST, instance=function)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:functions_organizers_list')
    else:
        form = FunctionsOfOrganizersForm(instance=function)
    return render(request, 'Accounting_button/functions_of_organizers/function_form.html', {'form': form, 'function': function})

@login_required
@permission_required('Accounting_button.delete_functions_of_organizers', raise_exception=True)
def delete_function_organizer(request, function_id):
    """
    Представление для удаления существующей функции организатора.
    Доступно только авторизованным пользователям с правом удаления функций организаторов.
    """
    function = get_object_or_404(Functions_of_organizers, id=function_id)
    
    if request.method == 'POST':
        try:
            function.delete()
            messages.success(request, 'Функция успешно удалена.')
        except ProtectedError:
            messages.error(request, 'Невозможно удалить эту функцию, так как она связана с другим объектом.', extra_tags='alert-danger')
        return redirect('Accounting_button:functions_organizers_list')
    
    return render(request, 'Accounting_button/functions_of_organizers/function_confirm_delete.html', {'function': function})

@login_required
@permission_required('Accounting_button.view_functions_of_organizers', raise_exception=True)
def functions_organizers_list(request):
    """
    Представление для отображения списка всех функций организаторов.
    Доступно только авторизованным пользователям с правом просмотра функций организаторов.
    """
    functions = Functions_of_organizers.objects.all()
    return render(request, 'Accounting_button/functions_of_organizers/functions_list.html', {'functions': functions})

