from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habit.

    Преобразует экземпляры модели Habit в JSON-формат и обратно.
    Обеспечивает вызов полной валидации модели (full_clean) для применения бизнес-правил.
    Используется для операций с отдельной привычкой и списками привычек.
    """

    class Meta:
        """
        Мета-опции для HabitSerializer.

        Определяет модель, с которой работает сериализатор,
        и поля для сериализации. В данном случае сериализуются все поля модели.
        Поля 'id', 'user', 'owner', 'created_at' доступны только для чтения.
        """

        model = Habit
        fields = (
            "id",
            "user",
            "owner",
            "action",
            "place",
            "time",
            "is_pleasant",
            "linked_habit",
            "reward",
            "frequency_days",
            "duration_seconds",
            "is_public",
            "created_at",
        )
        read_only_fields = ("id", "user", "owner", "created_at")

    def validate(self, data):
        """
        Выполняет валидацию данных перед созданием или обновлением привычки.

        Проверяет соблюдение бизнес-правил:
        - Приятная привычка не может иметь награду или быть связанной с другой привычкой.
        - Полезная привычка не может иметь и награду, и связанную приятную привычку одновременно.
        - Время выполнения не должно превышать 120 секунд.
        - Частота выполнения не может быть реже 1 раза в 7 дней.
        - Связанная привычка должна быть помечена как приятная.

        Аргумент:
            data (dict): Словарь с десериализованными данными.

        Возвращает:
            dict: Проверенные данные.

        Исключения:
            ValidationError: Если нарушены любые из вышеуказанных правил.
        """

        # 1. Нельзя одновременно указывать и связанную приятную привычку, и вознаграждение.
        if data.get("linked_habit") and data.get("reward"):
            raise serializers.ValidationError(
                "Выберите что-то одно: либо связанную приятную привычку, либо текстовое вознаграждение."
            )

        # 2. Время выполнения должно быть не больше 120 секунд.
        if data.get("duration_seconds", 0) > 120:
            raise serializers.ValidationError("Время на выполнение привычки не должно превышать 120 секунд")

        # 3. В связанные привычки могут попадать только привычки с признаком приятной привычки.
        linked_habit = data.get("linked_habit")
        if linked_habit and not linked_habit.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть помечена как приятная")

        # 4. У приятной привычки не может быть вознаграждения или связанной привычки.
        is_pleasant = data.get("is_pleasant", False)
        if is_pleasant and (data.get("reward") or data.get("linked_habit")):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки"
            )

        # 5. Частота выполнения не может быть реже 1 раза в 7 дней.
        if data.get("frequency_days", 0) > 7:
            raise serializers.ValidationError("Периодичность выполнения не может быть реже одного раза в неделю.")

        return data
