from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserCustomManager(BaseUserManager):
    """
    Кастомный менеджер для модели User.
    Обрабатывает создание обычных пользователей и суперпользователей.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создаёт и сохраняет обычного пользователя с указанными email и паролем.

        Аргументы:
            email (str): Адрес электронной почты пользователя.
            password (str, optional): Пароль пользователя. По умолчанию None.
            **extra_fields: Дополнительные поля для модели пользователя.

        Исключения:
            ValueError: Если не указан email или пароль.

        Возвращает:
            User: Созданный экземпляр пользователя.
        """

        if not email:
            raise ValueError("Поле электронной почты должно быть заполнено.")
        if password is None:
            raise ValueError("У пользователя должен быть пароль.")

        # Нормализация email (приведение к нижнему регистру для доменной части)
        email = self.normalize_email(email)

        # Создание экземпляра модели без сохранения в БД
        user = self.model(email=email, **extra_fields)

        # Безопасная установка пароля (хеширование)
        user.set_password(password)

        # Сохранение пользователя в базу данных
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создаёт и сохраняет суперпользователя с правами администратора.

        Аргументы:
            email (str): Адрес электронной почты суперпользователя.
            password (str, optional): Пароль суперпользователя. По умолчанию None.
            **extra_fields: Дополнительные поля для модели пользователя.

        Исключения:
            ValueError: Если у пользователя нет необходимых прав администратора.

        Возвращает:
            User: Созданный экземпляр суперпользователя.
        """

        # Устанавливаем флаги администратора по умолчанию, если они не были переданы
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Проверка, что все флаги администратора установлены в True
        if not all([extra_fields.get("is_staff"), extra_fields.get("is_superuser"), extra_fields.get("is_active")]):
            raise ValueError("Суперпользователь должен иметь is_staff=True, is_superuser=True и is_active=True.")

        # Используем логику создания обычного пользователя для сохранения
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя, использующая email в качестве логина."""

    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Укажите почту")
    first_name = models.CharField(max_length=30, verbose_name="Имя", blank=True, help_text="Введите ваше имя")
    last_name = models.CharField(max_length=30, verbose_name="Фамилия", blank=True, help_text="Введите вашу фамилию")
    date_joined = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    country = models.CharField(max_length=100, verbose_name="Страна", blank=True, help_text="Укажите страну")
    phone_number = models.CharField(
        max_length=35, verbose_name="Номер телефона", blank=True, help_text="Введите номер телефона"
    )
    bio = models.TextField(verbose_name="Информация о пользователе", blank=True, help_text="Расскажите немного о себе")
    avatar = models.ImageField(
        upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True, help_text="Загрузите аватар"
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=False, help_text="Определяет, может ли пользователь входить в систему. False до подтверждения email."
    )
    last_activity = models.DateTimeField(auto_now=True, help_text="Дата и время последней активности пользователя")

    objects = UserCustomManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """
        Мета-опции для модели User.

        Задаёт человеко-читаемые названия модели в единственном и множественном числе
        для отображения в админ-панели.
        """

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """
        Возвращает строковое представление объекта (email).

        Возвращает:
            str: Email пользователя.
        """
        return self.email

    def get_full_name(self):
        """
        Возвращает полное имя пользователя (Имя + Фамилия).

        Возвращает:
            str: Полное имя или email, если имя не указано.
        """
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def get_short_name(self):
        """
        Возвращает короткое имя пользователя.

        Возвращает:
            str: Имя или email, если имя не указано.
        """
        return self.first_name or self.email
