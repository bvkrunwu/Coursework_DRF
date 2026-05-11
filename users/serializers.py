from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """
    Базовый сериализатор для модели User.

    Используется для операций со списком пользователей и базовыми данными пользователя,
    включая управление правами доступа (is_staff, is_active).
    """

    class Meta:
        """
        Мета‑опции для UserSerializer.

        Определяет модель и полный набор полей для сериализации пользователя,
        включая идентификационные данные, контактную информацию и флаги доступа.
        """

        model = User
        fields = ["email", "password"]
