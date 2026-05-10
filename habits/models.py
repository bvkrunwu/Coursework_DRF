from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Habit(models.Model):
    """
    Модель для отслеживания привычек пользователя.

    Позволяет создавать как полезные, так и приятные привычки,
    связывать их между собой (полезная -> приятная в качестве награды)
    и задавать правила валидации.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь создавший привычку",
        related_name="created_habits",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        blank=True,
        null=True,
        help_text="Пользователь, обладающий правами на управление этой привычкой",
        related_name="owned_habits",
    )
    action = models.CharField(
        max_length=255, verbose_name="Действие", help_text="Краткое описание действия, которое вы будете выполнять"
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место выполнения",
        blank=True,
        null=True,
        help_text="Место, где выполняется действие (например: 'в офисе', 'дома')",
    )
    time = models.TimeField(
        verbose_name="Время", blank=True, null=True, help_text="Время, когда необходимо выполнять действие"
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Приятная привычка",
        help_text="Отметьте, если это привычка - вознаграждение. Не может иметь вознаграждение или связанную привычку",
    )
    linked_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная приятная привычка",
        blank=True,
        null=True,
        help_text="Выберите приятную привычку, "
        "которая будет наградой за выполнение этой (только для полезных привычек)",
        related_name="linked_to",
        limit_choices_to={"is_pleasant": True},
    )
    reward = models.CharField(
        max_length=255,
        verbose_name="Вознаграждение",
        blank=True,
        null=True,
        help_text="Опишите вознаграждение за выполнение полезной привычки "
        "(нельзя использовать вместе со связанной привычкой)",
    )
    frequency_days = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (дни)",
        help_text="Как часто повторять привычку (в днях). Не чаще 1 раза в 7 дней.",
    )
    duration_seconds = models.PositiveIntegerField(
        default=120,
        verbose_name="Время на выполнение (сек)",
        help_text="Предполагаемое время на выполнение привычки в секундах (максимум 120 секунд)",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичная привычка",
        help_text="Опубликовать привычку в общий доступ для других пользователей",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        """
        Мета-опции для модели Habit.

        Задаёт человеко-читаемые названия модели в единственном и множественном числе
        для отображения в админ-панели Django.
        """

        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        """
        Возвращает строковое представление объекта.

        Возвращает:
            str: Название привычки.
        """
        return self.action

    def clean(self):
        """
        Выполняет валидацию модели перед сохранением.

        Проверяет соблюдение бизнес-правил:
        - Приятная привычка не может иметь награду или быть связанной с другой привычкой.
        - Полезная привычка не может иметь и награду, и связанную приятную привычку одновременно.
        - Время выполнения не должно превышать 120 секунд.
        - Частота выполнения не может быть реже 1 раза в 7 дней.
        - Связанная привычка должна быть помечена как приятная.

        Исключения:
            ValidationError: Если нарушены любые из вышеуказанных правил.
        """
        super().clean()
        if self.user and self.owner and self.user != self.owner:
            raise ValidationError("Создатель привычки и её владелец должны совпадать.")

        # 1. Нельзя одновременно указывать и связанную приятную привычку, и вознаграждение.
        if self.linked_habit and self.reward:
            raise ValidationError(
                "Выберите что-то одно: либо связанную приятную привычку, либо текстовое вознаграждение."
            )

        # 2. Время выполнения должно быть не больше 120 секунд.
        if self.duration_seconds > 120:
            raise ValidationError("Время на выполнение привычки не должно превышать 120 секунд")

        # 3. В связанные привычки могут попадать только привычки с признаком приятной привычки.
        linked_habit = self.linked_habit
        if linked_habit and not linked_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной")

        # 4. Ограничения для приятной привычки
        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки")

        # 5. Частота выполнения не может быть реже 1 раза в 7 дней.
        if self.frequency_days > 7:
            raise ValidationError("Периодичность выполнения не может быть реже одного раза в неделю.")
