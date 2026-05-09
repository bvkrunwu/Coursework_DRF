from django.contrib import admin
from django.utils.timesince import timesince

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Административная модель для управления пользователями в Django Admin.

    Атрибуты:
        list_display (tuple): Поля, отображаемые в списке пользователей.
        list_editable (tuple): Поля, доступные для редактирования прямо из списка.
        list_filter (tuple): Поля для фильтрации пользователей.
        search_fields (tuple): Поля, по которым возможен поиск.
        ordering (tuple): Порядок сортировки пользователей.
        exclude (tuple): Поля, исключаемые из формы редактирования.
    """

    list_display = (
        "id",
        "email",
        "phone_number",
        "is_staff",
        "is_active",
        "user_groups",
        "date_joined",
        "get_last_activity_display",
    )
    list_editable = ("is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)
    exclude = ("password",)

    def get_queryset(self, request):
        """
        Возвращает оптимизированный QuerySet пользователей с предзагрузкой групп.

        Предзагрузка групп через prefetch_related предотвращает
        выполнение дополнительных запросов к базе данных при доступе к группам пользователя.

        Аргумент:
            request: Текущий HTTP-запрос.

        Возвращает:
            QuerySet: Пользователи с предзагруженными группами.
        """
        qs = super().get_queryset(request)
        return qs.prefetch_related("groups")

    def user_groups(self, obj):
        """
        Возвращает строковое представление групп пользователя.

        Если групп больше трёх, отображаются первые три и добавляется «и др.».

        Аргумент:
            obj (User): Объект пользователя.

        Возвращает:
            str: Список названий групп или «Нет групп».
        """
        groups = obj.groups.all()
        if not groups:
            return "Нет групп"
        group_names = [group.name for group in groups]
        if len(group_names) > 3:
            return f"{', '.join(group_names[:3])} и др."
        return ", ".join(group_names)

    user_groups.short_description = "Группы"

    def get_last_activity_display(self, obj):
        """
        Возвращает форматированное отображение последней активности пользователя.

        Показывает дату в формате «дд.мм.гггг чч:мм» и время, прошедшее с момента активности.

        Аргумент:
            obj (User): Объект пользователя.

        Возвращает:
            str: Форматированная строка с датой и временем или «Нет данных».
        """

        if obj.last_activity:
            formatted_date = obj.last_activity.strftime("%d.%m.%Y %H:%M")
            time_ago = timesince(obj.last_activity)
            return f"{formatted_date} ({time_ago} назад)"
        return "Нет данных"

    get_last_activity_display.short_description = "Последняя активность"
