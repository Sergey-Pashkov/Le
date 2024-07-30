# Импортируем необходимые модули и функции
from django.shortcuts import redirect

# Middleware для перенаправления пользователей после авторизации
class GroupRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Проверяем, аутентифицирован ли пользователь
        if request.user.is_authenticated:
            # Если пользователь авторизован, проверяем его путь
            if request.path == '/accounts/profile/':
                # Перенаправляем пользователя в зависимости от его группы
                if request.user.groups.filter(name='Собственник').exists():
                    return redirect('Accounting_button:owner_dashboard')
                elif request.user.groups.filter(name='Организатор').exists():
                    return redirect('Accounting_button:organizer_dashboard')
                elif request.user.groups.filter(name='Исполнитель').exists():
                    return redirect('Accounting_button:executor_dashboard')

        return response
