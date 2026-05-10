from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitCreateApiView(generics.CreateAPIView):
    """
    API‑представление для создания привычки.

    Позволяет аутентифицированным пользователям создавать новые привычки
    с автоматической установкой владельца.
    """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Выполняет сохранение нового объекта Habit.

        Автоматически устанавливает текущего пользователя (self.request.user)
        в качестве владельца (поле 'owner') создаваемой привычки.

        Аргумент:
            serializer (HabitSerializer): Сериализатор с валидированными данными.
        """
        serializer.save(user=self.request.user, owner=self.request.user)


class PublicHabitListApiView(generics.ListAPIView):
    """API‑представление для получения списка публичных привычек."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)


class HabitRetrieveApiView(generics.RetrieveAPIView):
    """
    API‑представление для просмотра детальной информации о привычке.

    Доступ к объекту разрешен
    только его владельцу и аутентифицированным пользователям.
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateApiView(generics.UpdateAPIView):
    """
    API‑представление для обновления привычки.

    Позволяет изменять существующие привычки.
    Доступ ограничен аутентифицированными пользователями, владельцами привычки.
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyApiView(generics.DestroyAPIView):
    """
    API‑представление для удаления привычки.

    Позволяет удалять привычку из системы.
    Доступ ограничен аутентифицированными пользователями или владельцами привычки.
    """

    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
