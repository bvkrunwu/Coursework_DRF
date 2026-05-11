from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserAPITestCase(APITestCase):
    """
    Набор тестов для проверки функциональности API пользователей.
    Включает тесты для регистрации, получения списка пользователей и детальной информации о пользователе.
    """

    def setUp(self):
        """
        Настройка тестовой среды перед каждым тестом.
        Создает пользователя и аутентифицирует его для последующих тестов.
        """

        self.user = User.objects.create(email="test_user@mail.ru")
        self.client.force_authenticate(user=self.user)

    def test_user_registration(self):
        """
        Тестирует регистрацию нового пользователя через API.
        Проверяет, что пользователь регистрируется с корректными данными и возвращается статус 201 CREATED.
        """

        url = reverse("users:users-list")
        data = {
            "email": "new_user@mail.ru",
            "password": "secure_password",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
