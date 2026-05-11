from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Habits API Documentation",
        default_version="v1",
        description="""
        Трекер привычек

        Цель проекта: Разработать бэкенд-сервис для SPA веб-приложения,
        помогающего пользователям формировать полезные привычки и отслеживать их выполнение.

        Концепция: Проект основан на концепции, изложенной в книге «Атомные привычки» Джеймса Клира.
        Каждая привычка описывается короткой фразой:

        > Я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО].

        Основные функции:
        - Создание, редактирование и удаление привычек.
        - Просмотр списка публичных привычек.
        - Система вознаграждений и связанных привычек.
        - Напоминания через Telegram.
        - Аутентификация через JWT.

        Технология:
        - Backend: Django REST Framework, PostgreSQL.
        - Frontend: React.js (SPA).
        - Интеграция: Telegram Bot API.
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ytfrpkkpreim@mail.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("", include("habits.urls", namespace="habits")),
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

# Только для режима разработки (DEBUG = True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
