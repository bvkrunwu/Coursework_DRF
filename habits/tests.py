from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.serializers import HabitSerializer
from users.models import User


class HabitAPITestCase(APITestCase):
    """
    Набор тестов для проверки функциональности API привычек.
    """

    def setUp(self):
        """
        Настройка тестовой среды перед каждым тестом.
        Создает пользователя и аутентифицирует его.
        """

        self.user = User.objects.create(email="test_user@mail.ru")
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            user=self.user,
            action="Бегать",
            place="Парковая зона",
            time="18:00:00",
            is_pleasant=False,
            reward="",
            frequency_days=1,
            duration_seconds=120,
            is_public=True,
            owner=self.user,
        )

    def test_habit_creation(self):
        """
        Тестирует создание новой привычки через API.
        Проверяет, что привычка создается с корректными данными.
        """

        url = reverse("habits:habit-create")
        data = {
            "action": "Новая привычка",
            "place": "Новый парк",
            "time": "19:00:00",
            "is_pleasant": False,
            "reward": "",
            "frequency_days": 1,
            "duration_seconds": 120,
            "is_public": True,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_habit_list(self):
        """
        Тестирует получение списка всех привычек.
        Проверяет, что ответ имеет статус 200 OK и содержит корректные данные.
        """

        url = reverse("habits:habit-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertGreater(len(data["results"]), 0)
        self.assertIn("Бегать", [item["action"] for item in data["results"]])

    def test_habit_retrieval(self):
        """
        Тестирует получение детальной информации о привычке по ее ID.
        Проверяет, что ответ имеет статус 200 OK.
        """

        url = reverse("habits:habit-detail", args=[self.habit.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["action"], "Бегать")

    def test_habit_update(self):
        """
        Тестирует обновление привычки через API.
        Проверяет, что привычка обновляется с новыми данными.
        """

        url = reverse("habits:habit-update", args=[self.habit.pk])
        new_data = {
            "action": "Измененная привычка",
            "place": "Другой парк",
            "time": "20:00:00",
            "is_pleasant": True,
            "reward": "",
            "frequency_days": 2,
            "duration_seconds": 90,
            "is_public": False,
        }

        response = self.client.put(url, new_data, format="json")

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_habit = Habit.objects.get(pk=self.habit.pk)
        self.assertEqual(updated_habit.action, "Измененная привычка")
        self.assertEqual(updated_habit.place, "Другой парк")

    def test_habit_delete(self):
        """
        Тестирует удаление привычки через API.
        Проверяет, что привычка удаляется успешно.
        """

        url = reverse("habits:habit-delete", args=[self.habit.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertRaises(Habit.DoesNotExist, Habit.objects.get, pk=self.habit.pk)

    def test_habit_serializer(self):
        """
        Тестирует сериализацию и десериализацию модели Habit.
        Проверяет, что все поля возвращаются корректно.
        """

        habit = Habit.objects.create(
            user=self.user,
            action="Тестовая привычка",
            place="Тестовое место",
            time="12:00:00",
            is_pleasant=False,
            reward="",
            frequency_days=1,
            duration_seconds=120,
            is_public=True,
            owner=self.user,
        )

        serializer = HabitSerializer(habit)
        data = serializer.data

        self.assertIn("id", data)
        self.assertIn("action", data)
        self.assertIn("place", data)
        self.assertIn("time", data)
        self.assertIn("is_pleasant", data)
        self.assertIn("reward", data)
        self.assertIn("frequency_days", data)
        self.assertIn("duration_seconds", data)
        self.assertIn("is_public", data)

        new_data = {
            "action": "Новая привычка",
            "place": "Новый парк",
            "time": "19:00:00",
            "is_pleasant": False,
            "reward": "",
            "frequency_days": 1,
            "duration_seconds": 120,
            "is_public": True,
        }

        serializer = HabitSerializer(data=new_data)
        self.assertTrue(serializer.is_valid())

        saved_habit = serializer.save(user=self.user, owner=self.user)
        self.assertEqual(saved_habit.action, "Новая привычка")
