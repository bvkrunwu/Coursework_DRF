from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями системы.

    Предоставляет полный набор операций CRUD для пользователей.
    Регистрация новых пользователей доступна без аутентификации,
    остальные операции требуют аутентификации.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Определяет классы разрешений в зависимости от выполняемого действия.

        Для создания пользователя (action == "create") разрешение AllowAny
        (регистрация доступна всем). Для всех остальных действий требуется
        аутентификация (IsAuthenticated).

        Возвращает:
            list: Список классов разрешений для текущего действия.
        """

        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Выполняет дополнительные действия при создании пользователя.

        Устанавливает флаг is_active=True и корректно сохраняет пароль
        с хешированием перед сохранением в базу данных.

        Аргументы:
            serializer (UserSerializer): Сериализатор с валидированными данными пользователя.
        """

        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
