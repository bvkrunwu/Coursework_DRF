from datetime import timedelta

import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from habits.models import Habit


@shared_task
def send_habit_notifications():
    """
    Периодическая задача отправки уведомлений в Telegram за 15 минут до начала выполнения привычки.
    """

    now = timezone.now()

    time_end = now + timedelta(minutes=15)

    habits = Habit.objects.filter(
        tg_chat_id__isnull=False,
        time__isnull=False,
        time__range=(now.time(), time_end.time()),
    )

    for habit in habits:
        action = habit.action or "выполнить привычку"
        place = f" в {habit.place}" if habit.place else ""
        text = f"Напоминание: мне нужно {action}{place} в {habit.time}."

        send_telegram_message(habit.tg_chat_id, text)


def send_telegram_message(chat_id, message):
    """Функция отправки уведомления в Telegram"""
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    url = f"{settings.TG_URL}{settings.TG_TOKEN}/sendMessage"

    try:
        requests.get(url, params=params)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке сообщения: {e}")
