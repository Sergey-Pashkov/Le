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














# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import TaxationSystems
from .forms import TaxationSystemsForm

@login_required
@permission_required('Accounting_button.add_taxationsystems', raise_exception=True)
def create_taxation_system(request):
    """
    Представление для создания новой налоговой системы.
    Доступно только авторизованным пользователям с правом добавления налоговых систем.
    """
    if request.method == 'POST':
        form = TaxationSystemsForm(request.POST)
        if form.is_valid():
            taxation_system = form.save(commit=False)
            taxation_system.owner = request.user  # Устанавливаем текущего пользователя как владельца
            taxation_system.save()
            return redirect('Accounting_button:taxation_systems_list')
    else:
        form = TaxationSystemsForm()
    return render(request, 'Accounting_button/taxation_systems/taxation_system_form.html', {'form': form})

@login_required
@permission_required('Accounting_button.view_taxationsystems', raise_exception=True)
def read_taxation_system(request, taxation_system_id):
    """
    Представление для отображения деталей налоговой системы.
    Доступно только авторизованным пользователям с правом просмотра налоговых систем.
    """
    taxation_system = get_object_or_404(TaxationSystems, id=taxation_system_id)
    return render(request, 'Accounting_button/taxation_systems/taxation_system_detail.html', {'taxation_system': taxation_system})

@login_required
@permission_required('Accounting_button.change_taxationsystems', raise_exception=True)
def update_taxation_system(request, taxation_system_id):
    """
    Представление для обновления существующей налоговой системы.
    Доступно только авторизованным пользователям с правом изменения налоговых систем.
    """
    taxation_system = get_object_or_404(TaxationSystems, id=taxation_system_id)
    if request.method == 'POST':
        form = TaxationSystemsForm(request.POST, instance=taxation_system)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:taxation_systems_list')
    else:
        form = TaxationSystemsForm(instance=taxation_system)
    return render(request, 'Accounting_button/taxation_systems/taxation_system_form.html', {'form': form, 'taxation_system': taxation_system})


from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from .models import TaxationSystems

@login_required
@permission_required('Accounting_button.delete_taxationsystems', raise_exception=True)
def delete_taxation_system(request, taxation_system_id):
    """
    Представление для удаления существующей налоговой системы.
    Доступно только авторизованным пользователям с правом удаления налоговых систем.
    """
    taxation_system = get_object_or_404(TaxationSystems, id=taxation_system_id)
    if request.method == 'POST':
        try:
            taxation_system.delete()
            messages.success(request, 'Налоговая система успешно удалена.')
        except ProtectedError:
            messages.error(request, 'Невозможно удалить эту налоговую систему, так как она связана с клиентами.', extra_tags='alert-danger')
        return redirect('Accounting_button:taxation_systems_list')
    return render(request, 'Accounting_button/taxation_systems/taxation_system_confirm_delete.html', {'taxation_system': taxation_system})








@login_required
@permission_required('Accounting_button.view_taxationsystems', raise_exception=True)
def taxation_systems_list(request):
    """
    Представление для отображения списка всех налоговых систем.
    Доступно только авторизованным пользователям с правом просмотра налоговых систем.
    """
    taxation_systems = TaxationSystems.objects.all()
    return render(request, 'Accounting_button/taxation_systems/taxation_systems_list.html', {'taxation_systems': taxation_systems})









from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from .models import GroupsOfTypesOfWork
from .forms import GroupsOfTypesOfWorkForm

# Представление для создания новой группы типов работ
@login_required
@permission_required('Accounting_button.add_groupsoftypesofwork', raise_exception=True)
def create_group(request):
    """
    Представление для создания новой группы типов работ.
    Доступно только авторизованным пользователям с правом добавления групп типов работ.
    """
    if request.method == 'POST':
        form = GroupsOfTypesOfWorkForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user  # Устанавливаем текущего пользователя как владельца
            group.save()
            return redirect('Accounting_button:groups_list')  # Перенаправление на список групп после сохранения
    else:
        form = GroupsOfTypesOfWorkForm()
    return render(request, 'Accounting_button/groups_of_types_of_work/group_form.html', {'form': form})

# Представление для отображения деталей группы типов работ
@login_required
@permission_required('Accounting_button.view_groupsoftypesofwork', raise_exception=True)
def read_group(request, group_id):
    """
    Представление для отображения деталей группы типов работ.
    Доступно только авторизованным пользователям с правом просмотра групп типов работ.
    """
    group = get_object_or_404(GroupsOfTypesOfWork, id=group_id)
    return render(request, 'Accounting_button/groups_of_types_of_work/group_detail.html', {'group': group})

# Представление для обновления существующей группы типов работ
@login_required
@permission_required('Accounting_button.change_groupsoftypesofwork', raise_exception=True)
def update_group(request, group_id):
    """
    Представление для обновления существующей группы типов работ.
    Доступно только авторизованным пользователям с правом изменения групп типов работ.
    """
    group = get_object_or_404(GroupsOfTypesOfWork, id=group_id)
    if request.method == 'POST':
        form = GroupsOfTypesOfWorkForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:groups_list')  # Перенаправление на список групп после обновления
    else:
        form = GroupsOfTypesOfWorkForm(instance=group)
    return render(request, 'Accounting_button/groups_of_types_of_work/group_form.html', {'form': form, 'group': group})

# Представление для удаления существующей группы типов работ
@login_required
@permission_required('Accounting_button.delete_groupsoftypesofwork', raise_exception=True)
def delete_group(request, group_id):
    """
    Представление для удаления существующей группы типов работ.
    Доступно только авторизованным пользователям с правом удаления групп типов работ.
    """
    group = get_object_or_404(GroupsOfTypesOfWork, id=group_id)
    if request.method == 'POST':
        try:
            group.delete()
            return redirect('Accounting_button:groups_list')  # Перенаправление на список групп после удаления
        except ProtectedError:
            # Отображаем сообщение об ошибке, если группа защищена
            error_message = "Невозможно удалить группу, так как существуют связанные с ней виды работ."
            return render(request, 'Accounting_button/groups_of_types_of_work/group_confirm_delete.html', {'group': group, 'error_message': error_message})
    return render(request, 'Accounting_button/groups_of_types_of_work/group_confirm_delete.html', {'group': group})

# Представление для отображения списка всех групп типов работ
@login_required
@permission_required('Accounting_button.view_groupsoftypesofwork', raise_exception=True)
def groups_list(request):
    """
    Представление для отображения списка всех групп типов работ.
    Доступно только авторизованным пользователям с правом просмотра групп типов работ.
    """
    groups = GroupsOfTypesOfWork.objects.all()
    return render(request, 'Accounting_button/groups_of_types_of_work/groups_list.html', {'groups': groups})














from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import TypesOfJobs, GroupsOfTypesOfWork
from .forms import TypesOfJobsForm

@login_required
@permission_required('Accounting_button.add_typesofjobs', raise_exception=True)
def create_type_of_job(request):
    """
    Представление для создания нового типа работы.
    Доступно только авторизованным пользователям с правом добавления типов работ.
    """
    if request.method == 'POST':
        form = TypesOfJobsForm(request.POST)
        if form.is_valid():
            type_of_job = form.save(commit=False)
            type_of_job.owner = request.user  # Устанавливаем текущего пользователя как владельца
            type_of_job.save()
            return redirect('Accounting_button:types_of_jobs_list')
    else:
        form = TypesOfJobsForm()
    return render(request, 'Accounting_button/types_of_jobs/type_of_job_form.html', {'form': form, 'type_of_job': None})

@login_required
@permission_required('Accounting_button.view_typesofjobs', raise_exception=True)
def read_type_of_job(request, type_of_job_id):
    """
    Представление для отображения деталей типа работы.
    Доступно только авторизованным пользователям с правом просмотра типов работ.
    """
    type_of_job = get_object_or_404(TypesOfJobs, id=type_of_job_id)
    return render(request, 'Accounting_button/types_of_jobs/type_of_job_detail.html', {'type_of_job': type_of_job})

@login_required
@permission_required('Accounting_button.change_typesofjobs', raise_exception=True)
def update_type_of_job(request, type_of_job_id):
    """
    Представление для обновления существующего типа работы.
    Доступно только авторизованным пользователям с правом изменения типов работ.
    """
    type_of_job = get_object_or_404(TypesOfJobs, id=type_of_job_id)
    if request.method == 'POST':
        form = TypesOfJobsForm(request.POST, instance=type_of_job)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:types_of_jobs_list')
    else:
        form = TypesOfJobsForm(instance=type_of_job)
    return render(request, 'Accounting_button/types_of_jobs/type_of_job_form.html', {'form': form, 'type_of_job': type_of_job})



from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from .models import TypesOfJobs

@login_required
@permission_required('Accounting_button.delete_typesofjobs', raise_exception=True)
def delete_type_of_job(request, type_of_job_id):
    """
    Представление для удаления существующего типа работы.
    Доступно только авторизованным пользователям с правом удаления типов работ.
    """
    # Получаем объект типа работы или возвращаем 404 ошибку, если он не найден
    type_of_job = get_object_or_404(TypesOfJobs, id=type_of_job_id)
    error_message = None  # Переменная для хранения сообщения об ошибке

    if request.method == 'POST':
        try:
            # Пытаемся удалить объект типа работы
            type_of_job.delete()
            # Перенаправляем пользователя на список типов работ после успешного удаления
            return redirect('Accounting_button:types_of_jobs_list')
        except ProtectedError:
            # Если возникает ошибка ProtectedError, задаем сообщение об ошибке
            error_message = (
                "Невозможно удалить тип работы, так как существуют связанные записи в журнале стандартных операций."
            )
    
    # Отображаем страницу подтверждения удаления с возможным сообщением об ошибке
    return render(request, 'Accounting_button/types_of_jobs/type_of_job_confirm_delete.html', {'type_of_job': type_of_job, 'error_message': error_message})




from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import GroupsOfTypesOfWork, TypesOfJobs

@login_required
@permission_required('Accounting_button.view_typesofjobs', raise_exception=True)
def types_of_jobs_list(request):
    """
    Представление для отображения списка всех типов работ, сгруппированных по группе.
    Доступно только авторизованным пользователям с правом просмотра типов работ.
    """
    groups = GroupsOfTypesOfWork.objects.all().order_by('name')
    grouped_jobs = {group: TypesOfJobs.objects.filter(group=group).order_by('name') for group in groups}
    total_jobs = TypesOfJobs.objects.count()  # Подсчитываем общее количество типов работ
    return render(request, 'Accounting_button/types_of_jobs/types_of_jobs_list.html', {
        'grouped_jobs': grouped_jobs,
        'total_jobs': total_jobs  # Передаем общее количество типов работ в контекст
    })















# Accounting_button/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import ProtectedError
from .models import PerformersRates, OrganizersRates
from .forms import PerformersRatesForm, OrganizersRatesForm

# Представления для тарифов исполнителей
@login_required
@permission_required('Accounting_button.add_performersrates', raise_exception=True)
def create_performers_rate(request):
    if request.method == 'POST':
        form = PerformersRatesForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.owner = request.user
            rate.save()
            return redirect('Accounting_button:rates_list')
    else:
        form = PerformersRatesForm()
    return render(request, 'Accounting_button/performers_rates/rate_form.html', {'form': form})

@login_required
@permission_required('Accounting_button.view_performersrates', raise_exception=True)
def read_performers_rate(request, rate_id):
    rate = get_object_or_404(PerformersRates, id=rate_id)
    return render(request, 'Accounting_button/performers_rates/rate_detail.html', {'rate': rate})

@login_required
@permission_required('Accounting_button.change_performersrates', raise_exception=True)
def update_performers_rate(request, rate_id):
    rate = get_object_or_404(PerformersRates, id=rate_id)
    if request.method == 'POST':
        form = PerformersRatesForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:rates_list')
    else:
        form = PerformersRatesForm(instance=rate)
    return render(request, 'Accounting_button/performers_rates/rate_form.html', {'form': form, 'rate': rate})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import ProtectedError
from .models import PerformersRates

@login_required
@permission_required('Accounting_button.delete_performersrates', raise_exception=True)
def delete_performers_rate(request, rate_id):
    """
    Представление для удаления существующего тарифа исполнителя.
    Доступно только авторизованным пользователям с правом удаления тарифов исполнителей.
    """
    rate = get_object_or_404(PerformersRates, id=rate_id)
    if request.method == 'POST':
        try:
            rate.delete()
            messages.success(request, 'Тариф успешно удален.')
        except ProtectedError as e:
            # Получаем связанные модели из исключения
            related_objects = e.protected_objects
            related_model_names = ', '.join(set(obj._meta.verbose_name for obj in related_objects))
            messages.error(
                request, 
                f'Невозможно удалить этот тариф, так как он связан с записями в следующих моделях: {related_model_names}.',
                extra_tags='alert-danger'
            )
        return redirect('Accounting_button:rates_list')
    return render(request, 'Accounting_button/performers_rates/rate_confirm_delete.html', {'rate': rate})




@login_required
@permission_required('Accounting_button.view_performersrates', raise_exception=True)
def rates_list(request):
    rates = PerformersRates.objects.all()
    return render(request, 'Accounting_button/performers_rates/rates_list.html', {'rates': rates})

# Представления для ставок организаторов
@login_required
@permission_required('Accounting_button.add_organizersrates', raise_exception=True)
def create_organizers_rate(request):
    if request.method == 'POST':
        form = OrganizersRatesForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.owner = request.user
            rate.save()
            return redirect('Accounting_button:organizers_rates_list')
    else:
        form = OrganizersRatesForm()
    return render(request, 'Accounting_button/organizers_rates/rate_form.html', {'form': form})

@login_required
@permission_required('Accounting_button.view_organizersrates', raise_exception=True)
def read_organizers_rate(request, rate_id):
    rate = get_object_or_404(OrganizersRates, id=rate_id)
    return render(request, 'Accounting_button/organizers_rates/rate_detail.html', {'rate': rate})

@login_required
@permission_required('Accounting_button.change_organizersrates', raise_exception=True)
def update_organizers_rate(request, rate_id):
    rate = get_object_or_404(OrganizersRates, id=rate_id)
    if request.method == 'POST':
        form = OrganizersRatesForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:organizers_rates_list')
    else:
        form = OrganizersRatesForm(instance=rate)
    return render(request, 'Accounting_button/organizers_rates/rate_form.html', {'form': form, 'rate': rate})

@login_required
@permission_required('Accounting_button.delete_organizersrates', raise_exception=True)
def delete_organizers_rate(request, rate_id):
    rate = get_object_or_404(OrganizersRates, id=rate_id)
    if request.method == 'POST':
        try:
            rate.delete()
            messages.success(request, 'Ставка успешно удалена.')
        except ProtectedError:
            messages.error(request, 'Невозможно удалить эту ставку, так как она связана с другим объектом.', extra_tags='alert-danger')
        return redirect('Accounting_button:organizers_rates_list')
    return render(request, 'Accounting_button/organizers_rates/rate_confirm_delete.html', {'rate': rate})

@login_required
@permission_required('Accounting_button.view_organizersrates', raise_exception=True)
def organizers_rates_list(request):
    rates = OrganizersRates.objects.all()
    return render(request, 'Accounting_button/organizers_rates/rates_list.html', {'rates': rates})




import openpyxl
from django.http import HttpResponse

@login_required
def export_types_of_jobs_to_excel(request):
    """
    Представление для экспорта типов работ в Excel.
    Доступно только авторизованным пользователям.
    """
    # Создаем книгу и лист
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Types of Jobs"

    # Добавляем заголовки
    headers = ["ID", "Name", "Description", "Time Standard", "Tariff Name", "Tariff", "Group", "Owner"]
    ws.append(headers)

    # Получаем данные
    types_of_jobs = TypesOfJobs.objects.all()

    for job in types_of_jobs:
        ws.append([
            job.id,
            job.name,
            job.description,
            job.time_standard,
            job.tariff_name.name,
            job.tariff_name.cost_per_minute,
            job.group.name,
            job.owner.username if job.owner else 'N/A'
        ])

    # Настраиваем HTTP ответ
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=types_of_jobs.xlsx'

    # Сохраняем книгу в HTTP ответ
    wb.save(response)
    return response


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Clients, TaxationSystems
from .forms import ClientsForm

@login_required
def create_client(request):
    """
    Представление для создания нового клиента.
    Доступно только авторизованным пользователям.
    """
    if request.method == 'POST':
        form = ClientsForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.owner = request.user  # Устанавливаем текущего пользователя как владельца
            client.save()
            return redirect('Accounting_button:clients_list')
    else:
        form = ClientsForm()
    return render(request, 'Accounting_button/clients/client_form.html', {'form': form, 'client': None})




from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Clients

@login_required
def read_client(request, client_id):
    """
    Представление для отображения деталей клиента.
    Доступно только авторизованным пользователям.
    """
    client = get_object_or_404(Clients, id=client_id)
    return render(request, 'Accounting_button/clients/client_detail.html', {'client': client})







@login_required
def update_client(request, client_id):
    """
    Представление для обновления существующего клиента.
    Доступно только авторизованным пользователям.
    """
    client = get_object_or_404(Clients, id=client_id)
    if request.method == 'POST':
        form = ClientsForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:clients_list')
    else:
        form = ClientsForm(instance=client)
    return render(request, 'Accounting_button/clients/client_form.html', {'form': form, 'client': client})



from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from .models import Clients

@login_required
def delete_client(request, client_id):
    """
    Представление для удаления существующего клиента.
    Доступно только авторизованным пользователям.
    """
    client = get_object_or_404(Clients, id=client_id)
    error_message = None

    if request.method == 'POST':
        try:
            client.delete()
            return redirect('Accounting_button:clients_list')
        except ProtectedError:
            error_message = (
                "Невозможно удалить клиента, так как существуют связанные записи в журнале стандартных операций."
            )
    
    return render(request, 'Accounting_button/clients/client_confirm_delete.html', {'client': client, 'error_message': error_message})





@login_required
def clients_list(request):
    """
    Представление для отображения списка всех клиентов, сгруппированных по налоговой системе.
    Доступно только авторизованным пользователям.
    """
    tax_systems = TaxationSystems.objects.all().order_by('name')
    grouped_clients = {tax_system: Clients.objects.filter(tax_system=tax_system).order_by('short_title') for tax_system in tax_systems}
    total_clients = Clients.objects.count()
    return render(request, 'Accounting_button/clients/clients_list.html', {
        'grouped_clients': grouped_clients,
        'total_clients': total_clients
    })

import openpyxl
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Clients

@login_required
def export_clients_to_excel(request):
    """
    Представление для экспорта клиентов в Excel.
    Доступно только авторизованным пользователям.
    """
    # Создаем книгу и лист
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Clients"

    # Добавляем заголовки
    headers = [
        "ID", "Short Title", "Full Name", "Contract Price", "INN", "Contract Number and Date",
        "Tax System", "Activities", "Number of Nomenclature Groups", "Contact Person",
        "Telephone", "Email", "Mailing Address", "Hide in Search", "Comments", "Owner"
    ]
    ws.append(headers)

    # Получаем данные
    clients = Clients.objects.all()

    for client in clients:
        ws.append([
            client.id,
            client.short_title,
            client.full_name,
            client.contract_price,
            client.inn,
            client.contract_number_and_date,
            client.tax_system.name,
            client.activities,
            client.number_of_nomenclature_groups,
            client.contact_person,
            client.telephone,
            client.email,
            client.mailing_address,
            "Yes" if client.hide_in_search else "No",
            client.comments,
            client.owner.username if client.owner else 'N/A'
        ])

    # Настраиваем HTTP ответ
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=clients.xlsx'

    # Сохраняем книгу в HTTP ответ
    wb.save(response)
    return response



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from .models import StandardOperationsLog
from .forms import StandardOperationsLogForm

def user_belongs_to_group(user, group_name):
    """
    Проверяет, принадлежит ли пользователь к определенной группе.
    """
    return user.groups.filter(name=group_name).exists()

@login_required
@permission_required('Accounting_button.add_standardoperationslog', raise_exception=True)
def create_standard_operations_log(request):
    """
    Представление для создания новой записи в журнале стандартных операций.
    Доступно только авторизованным пользователям с правом добавления записей.
    """
    if request.method == 'POST':
        form = StandardOperationsLogForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:standard_operations_log_list')
    else:
        form = StandardOperationsLogForm()
        # Сортировка клиентов и типов работ по ID
        form.fields['client'].queryset = form.fields['client'].queryset.order_by('id')
        form.fields['type_of_work'].queryset = form.fields['type_of_work'].queryset.order_by('id')
    return render(request, 'Accounting_button/standard_operations_log/standard_operations_log_form.html', {'form': form})

@login_required
@permission_required('Accounting_button.view_standardoperationslog', raise_exception=True)
def read_standard_operations_log(request, log_id):
    """
    Представление для отображения деталей записи в журнале стандартных операций.
    Доступно только авторизованным пользователям с правом просмотра записей.
    """
    log = get_object_or_404(StandardOperationsLog, id=log_id)
    if log.owner != request.user and user_belongs_to_group(request.user, "Исполнитель"):
        return redirect('Accounting_button:standard_operations_log_list')
    return render(request, 'Accounting_button/standard_operations_log/standard_operations_log_detail.html', {'log': log})

@login_required
@permission_required('Accounting_button.change_standardoperationslog', raise_exception=True)
def update_standard_operations_log(request, log_id):
    """
    Представление для обновления существующей записи в журнале стандартных операций.
    Доступно только авторизованным пользователям с правом изменения записей.
    """
    log = get_object_or_404(StandardOperationsLog, id=log_id)
    if log.owner != request.user and user_belongs_to_group(request.user, "Исполнитель"):
        return redirect('Accounting_button:standard_operations_log_list')
    
    if request.method == 'POST':
        form = StandardOperationsLogForm(request.POST, instance=log, request=request)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:standard_operations_log_list')
    else:
        form = StandardOperationsLogForm(instance=log)
        # Сортировка клиентов и типов работ по ID
        form.fields['client'].queryset = form.fields['client'].queryset.order_by('id')
        form.fields['type_of_work'].queryset = form.fields['type_of_work'].queryset.order_by('id')
    return render(request, 'Accounting_button/standard_operations_log/standard_operations_log_form.html', {'form': form, 'log': log})

@login_required
@permission_required('Accounting_button.delete_standardoperationslog', raise_exception=True)
def delete_standard_operations_log(request, log_id):
    """
    Представление для удаления существующей записи в журнале стандартных операций.
    Доступно только авторизованным пользователям с правом удаления записей.
    """
    log = get_object_or_404(StandardOperationsLog, id=log_id)
    if log.owner != request.user and user_belongs_to_group(request.user, "Исполнитель"):
        return redirect('Accounting_button:standard_operations_log_list')
    
    if request.method == 'POST':
        log.delete()
        return redirect('Accounting_button:standard_operations_log_list')
    return render(request, 'Accounting_button/standard_operations_log/standard_operations_log_confirm_delete.html', {'log': log})

@login_required
@permission_required('Accounting_button.view_standardoperationslog', raise_exception=True)
def standard_operations_log_list(request):
    """
    Представление для отображения списка всех записей в журнале стандартных операций,
    сгруппированных по владельцу. Фильтрация по текущему месяцу.
    Доступно только авторизованным пользователям с правом просмотра записей.
    """
    current_month = timezone.now().month
    current_year = timezone.now().year
    if user_belongs_to_group(request.user, "Исполнитель"):
        logs_by_owner = StandardOperationsLog.objects.filter(owner=request.user, date__year=current_year, date__month=current_month).order_by('owner')
    else:
        logs_by_owner = StandardOperationsLog.objects.filter(date__year=current_year, date__month=current_month).order_by('owner')
    
    grouped_logs = {}
    for log in logs_by_owner:
        if log.owner not in grouped_logs:
            grouped_logs[log.owner] = []
        grouped_logs[log.owner].append(log)
    
    return render(request, 'Accounting_button/standard_operations_log/standard_operations_log_list.html', {'grouped_logs': grouped_logs})







from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import NonStandardOperationsLog
from .forms import NonStandardOperationsLogForm
from django.db.models import ProtectedError

def user_belongs_to_group(user, group_name):
    """
    Проверяет, принадлежит ли пользователь к определенной группе.
    """
    return user.groups.filter(name=group_name).exists()

@login_required
def create_non_standard_operations_log(request):
    """
    Представление для создания новой записи в журнале нестандартных операций.
    Доступно только авторизованным пользователям.
    """
    if request.method == 'POST':
        form = NonStandardOperationsLogForm(request.POST, request=request)
        if form.is_valid():
            non_standard_log = form.save(commit=False)
            if not non_standard_log.owner:
                non_standard_log.owner = request.user  # Устанавливаем владельца записи
            non_standard_log.save()
            return redirect('Accounting_button:non_standard_operations_log_list')
    else:
        form = NonStandardOperationsLogForm()
        # Сортировка клиентов и тарифов по ID
        form.fields['client'].queryset = form.fields['client'].queryset.order_by('id')
        form.fields['rate'].queryset = form.fields['rate'].queryset.order_by('id')
    return render(request, 'Accounting_button/non_standard_operations_log/non_standard_operations_log_form.html', {'form': form})

@login_required
def read_non_standard_operations_log(request, log_id):
    """
    Представление для отображения деталей записи в журнале нестандартных операций.
    Доступно только авторизованным пользователям.
    """
    log = get_object_or_404(NonStandardOperationsLog, id=log_id)
    if log.owner != request.user and user_belongs_to_group(request.user, "Исполнитель"):
        return redirect('Accounting_button:non_standard_operations_log_list')
    return render(request, 'Accounting_button/non_standard_operations_log/non_standard_operations_log_detail.html', {'log': log})

@login_required
def update_non_standard_operations_log(request, log_id):
    """
    Представление для обновления существующей записи в журнале нестандартных операций.
    Доступно только авторизованным пользователям.
    """
    log = get_object_or_404(NonStandardOperationsLog, id=log_id)
    if log.owner != request.user and user_belongs_to_group(request.user, "Исполнитель"):
        return redirect('Accounting_button:non_standard_operations_log_list')
    
    if request.method == 'POST':
        form = NonStandardOperationsLogForm(request.POST, instance=log, request=request)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:non_standard_operations_log_list')
    else:
        form = NonStandardOperationsLogForm(instance=log)
        # Сортировка клиентов и тарифов по ID
        form.fields['client'].queryset = form.fields['client'].queryset.order_by('id')
        form.fields['rate'].queryset = form.fields['rate'].queryset.order_by('id')
    return render(request, 'Accounting_button/non_standard_operations_log/non_standard_operations_log_form.html', {'form': form, 'log': log})

@login_required
def delete_non_standard_operations_log(request, log_id):
    """
    Представление для удаления существующей записи в журнале нестандартных операций.
    Доступно только авторизованным пользователям.
    """
    log = get_object_or_404(NonStandardOperationsLog, id=log_id)
    if log.owner != request.user and user_belongs_to_group(request.user, "Исполнитель"):
        return redirect('Accounting_button:non_standard_operations_log_list')
    
    if request.method == 'POST':
        try:
            log.delete()
            return redirect('Accounting_button:non_standard_operations_log_list')
        except ProtectedError:
            return render(request, 'Accounting_button/non_standard_operations_log/non_standard_operations_log_confirm_delete.html', {
                'log': log,
                'error_message': 'Невозможно удалить запись, так как она связана с другими записями.'
            })
    return render(request, 'Accounting_button/non_standard_operations_log/non_standard_operations_log_confirm_delete.html', {'log': log})

@login_required
def non_standard_operations_log_list(request):
    """
    Представление для отображения списка всех записей в журнале нестандартных операций,
    сгруппированных по владельцу.
    Доступно только авторизованным пользователям.
    """
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    if user_belongs_to_group(request.user, "Исполнитель"):
        logs_by_owner = NonStandardOperationsLog.objects.filter(owner=request.user, date__year=current_year, date__month=current_month).order_by('owner')
    else:
        logs_by_owner = NonStandardOperationsLog.objects.filter(date__year=current_year, date__month=current_month).order_by('owner')
    
    grouped_logs = {}
    for log in logs_by_owner:
        if log.owner not in grouped_logs:
            grouped_logs[log.owner] = []
        grouped_logs[log.owner].append(log)
    
    return render(request, 'Accounting_button/non_standard_operations_log/non_standard_operations_log_list.html', {'grouped_logs': grouped_logs})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from django.contrib import messages
from .models import TypesOfIncome
from .forms import TypesOfIncomeForm

@login_required
@permission_required('Accounting_button.add_typesofincome', raise_exception=True)
def create_type_of_income(request):
    """
    Представление для создания нового типа дохода.
    Доступно только авторизованным пользователям с правом добавления типов доходов.
    """
    if request.method == 'POST':
        form = TypesOfIncomeForm(request.POST)
        if form.is_valid():
            type_of_income = form.save(commit=False)
            type_of_income.owner = request.user  # Устанавливаем текущего пользователя как владельца
            type_of_income.save()
            return redirect('Accounting_button:types_of_income_list')
    else:
        form = TypesOfIncomeForm()
    return render(request, 'Accounting_button/types_of_income/type_of_income_form.html', {'form': form})

@login_required
@permission_required('Accounting_button.view_typesofincome', raise_exception=True)
def read_type_of_income(request, type_id):
    """
    Представление для отображения деталей типа дохода.
    Доступно только авторизованным пользователям с правом просмотра типов доходов.
    """
    type_of_income = get_object_or_404(TypesOfIncome, id=type_id)
    return render(request, 'Accounting_button/types_of_income/type_of_income_detail.html', {'type_of_income': type_of_income})

@login_required
@permission_required('Accounting_button.change_typesofincome', raise_exception=True)
def update_type_of_income(request, type_id):
    """
    Представление для обновления существующего типа дохода.
    Доступно только авторизованным пользователям с правом изменения типов доходов.
    """
    type_of_income = get_object_or_404(TypesOfIncome, id=type_id)
    if request.method == 'POST':
        form = TypesOfIncomeForm(request.POST, instance=type_of_income)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:types_of_income_list')
    else:
        form = TypesOfIncomeForm(instance=type_of_income)
    return render(request, 'Accounting_button/types_of_income/type_of_income_form.html', {'form': form, 'type_of_income': type_of_income})

@login_required
@permission_required('Accounting_button.delete_typesofincome', raise_exception=True)
def delete_type_of_income(request, type_id):
    """
    Представление для удаления существующего типа дохода.
    Доступно только авторизованным пользователям с правом удаления типов доходов.
    """
    type_of_income = get_object_or_404(TypesOfIncome, id=type_id)
    if request.method == 'POST':
        try:
            type_of_income.delete()
            messages.success(request, 'Тип дохода успешно удалён.')
        except ProtectedError:
            messages.error(request, 'Невозможно удалить этот тип дохода, так как он связан с другими записями.')
        return redirect('Accounting_button:types_of_income_list')
    return render(request, 'Accounting_button/types_of_income/type_of_income_confirm_delete.html', {'type_of_income': type_of_income})

@login_required
@permission_required('Accounting_button.view_typesofincome', raise_exception=True)
def types_of_income_list(request):
    """
    Представление для отображения списка всех типов доходов.
    Доступно только авторизованным пользователям с правом просмотра типов доходов.
    """
    types_of_income = TypesOfIncome.objects.all()
    return render(request, 'Accounting_button/types_of_income/types_of_income_list.html', {'types_of_income': types_of_income})




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import TypesOfExpenses
from .forms import TypesOfExpensesForm

@login_required
@permission_required('Accounting_button.view_typesofexpenses', raise_exception=True)
def types_of_expenses_list(request):
    types_of_expenses = TypesOfExpenses.objects.all()
    return render(request, 'Accounting_button/types_of_expenses/types_of_expenses_list.html', {'types_of_expenses': types_of_expenses})

@login_required
@permission_required('Accounting_button.view_typesofexpenses', raise_exception=True)
def read_type_of_expense(request, expense_id):
    type_of_expense = get_object_or_404(TypesOfExpenses, id=expense_id)
    return render(request, 'Accounting_button/types_of_expenses/type_of_expense_detail.html', {'type_of_expense': type_of_expense})

@login_required
@permission_required('Accounting_button.add_typesofexpenses', raise_exception=True)
def create_type_of_expense(request):
    if request.method == 'POST':
        form = TypesOfExpensesForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.owner = request.user
            expense.save()
            return redirect('Accounting_button:types_of_expenses_list')
    else:
        form = TypesOfExpensesForm()
    return render(request, 'Accounting_button/types_of_expenses/type_of_expense_form.html', {'form': form})

@login_required
@permission_required('Accounting_button.change_typesofexpenses', raise_exception=True)
def update_type_of_expense(request, expense_id):
    type_of_expense = get_object_or_404(TypesOfExpenses, id=expense_id)
    if request.method == 'POST':
        form = TypesOfExpensesForm(request.POST, instance=type_of_expense)
        if form.is_valid():
            form.save()
            return redirect('Accounting_button:types_of_expenses_list')
    else:
        form = TypesOfExpensesForm(instance=type_of_expense)
    return render(request, 'Accounting_button/types_of_expenses/type_of_expense_form.html', {'form': form, 'type_of_expense': type_of_expense})

@login_required
@permission_required('Accounting_button.delete_typesofexpenses', raise_exception=True)
def delete_type_of_expense(request, expense_id):
    type_of_expense = get_object_or_404(TypesOfExpenses, id=expense_id)
    if request.method == 'POST':
        type_of_expense.delete()
        return redirect('Accounting_button:types_of_expenses_list')
    return render(request, 'Accounting_button/types_of_expenses/type_of_expense_confirm_delete.html', {'type_of_expense': type_of_expense})





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.timezone import now
from .models import IncomeJournal
from .forms import IncomeJournalForm

def is_current_month(date):
    """
    Проверяет, относится ли дата к текущему месяцу.
    Args:
        date (datetime.date): Дата для проверки.
    Returns:
        bool: True, если дата в текущем месяце, иначе False.
    """
    today = now().date()
    return date.year == today.year and date.month == today.month




from django.db.models import Sum
from django.utils.timezone import localdate

@login_required
@permission_required('Accounting_button.view_incomejournal', raise_exception=True)
def income_journal_list(request):
    """
    Просмотр списка записей IncomeJournal за текущий месяц.
    Фильтрует записи журнала доходов по текущему месяцу и отображает их в виде списка.
    Записи упорядочиваются по ID. 
    Также отображается информация о количестве записей за сегодняшний день, итоговой сумме и статистика по займам.
    """
    today = localdate()  # Получаем текущую дату
    journals = IncomeJournal.objects.filter(date_of_event__month=now().month).order_by('id')

    # Количество и сумма записей за сегодняшний день
    today_count = IncomeJournal.objects.filter(date__date=today).count()
    today_sum = IncomeJournal.objects.filter(date__date=today).aggregate(Sum('value'))['value__sum'] or 0

    # Количество и сумма по займам за сегодняшний день
    loans_count = IncomeJournal.objects.filter(date__date=today, name__name="Займы").count()
    loans_sum = IncomeJournal.objects.filter(date__date=today, name__name="Займы").aggregate(Sum('value'))['value__sum'] or 0

    return render(request, 'Accounting_button/income_journal/income_journal_list.html', {
        'journals': journals,
        'today_count': today_count,
        'today_sum': today_sum,
        'loans_count': loans_count,
        'loans_sum': loans_sum,
    })



@login_required
@permission_required('Accounting_button.view_incomejournal', raise_exception=True)
def read_income_journal(request, journal_id):
    """
    Просмотр деталей конкретной записи IncomeJournal.

    Проверяет, относится ли запись к текущему месяцу. Если нет, перенаправляет на список записей.
    """
    journal = get_object_or_404(IncomeJournal, id=journal_id)
    if not is_current_month(journal.date_of_event):
        return redirect('Accounting_button:income_journal_list')
    return render(request, 'Accounting_button/income_journal/income_journal_detail.html', {'journal': journal})






@login_required
@permission_required('Accounting_button.add_incomejournal', raise_exception=True)
def create_income_journal(request):
    """
    Создание новой записи IncomeJournal.
    """
    if request.method == 'POST':
        form = IncomeJournalForm(request.POST)
        if form.is_valid():
            journal = form.save(commit=False)
            if journal.name.name == 'Займы':
                journal.client = None  # Очищаем поле client, если выбрано "Займы"
            journal.owner = request.user  # Автоматическое заполнение поля owner текущим пользователем
            journal.save()
            return redirect('Accounting_button:income_journal_list')
    else:
        form = IncomeJournalForm()
    return render(request, 'Accounting_button/income_journal/income_journal_form.html', {'form': form})

@login_required
@permission_required('Accounting_button.change_incomejournal', raise_exception=True)
def update_income_journal(request, journal_id):
    """
    Редактирование существующей записи IncomeJournal.
    """
    journal = get_object_or_404(IncomeJournal, id=journal_id)
    if not is_current_month(journal.date_of_event):
        return redirect('Accounting_button:income_journal_list')

    if request.method == 'POST':
        form = IncomeJournalForm(request.POST, instance=journal)
        if form.is_valid():
            journal = form.save(commit=False)
            if journal.name.name == 'Займы':
                journal.client = None  # Очищаем поле client, если выбрано "Займы"
            journal.save()
            return redirect('Accounting_button:income_journal_list')
    else:
        form = IncomeJournalForm(instance=journal)
    return render(request, 'Accounting_button/income_journal/income_journal_form.html', {'form': form, 'journal': journal})













@login_required
@permission_required('Accounting_button.delete_incomejournal', raise_exception=True)
def delete_income_journal(request, journal_id):
    """
    Удаление записи IncomeJournal.

    Позволяет удалить запись, если она относится к текущему месяцу.
    В случае ошибки защищенного удаления, выводит сообщение об ошибке.
    """
    journal = get_object_or_404(IncomeJournal, id=journal_id)
    if not is_current_month(journal.date_of_event):
        return redirect('Accounting_button:income_journal_list')

    if request.method == 'POST':
        try:
            journal.delete()
            return redirect('Accounting_button:income_journal_list')
        except models.ProtectedError:
            error_message = "Невозможно удалить запись, так как она связана с другими объектами."
            return render(request, 'Accounting_button/income_journal/income_journal_confirm_delete.html', {'journal': journal, 'error_message': error_message})
    return render(request, 'Accounting_button/income_journal/income_journal_confirm_delete.html', {'journal': journal})
