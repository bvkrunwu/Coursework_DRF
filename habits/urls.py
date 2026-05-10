from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (
    HabitCreateApiView,
    HabitDestroyApiView,
    HabitRetrieveApiView,
    HabitUpdateApiView,
    PublicHabitListApiView,
)

app_name = HabitsConfig.name


urlpatterns = [
    path("habits/create/", HabitCreateApiView.as_view(), name="habit-create"),
    path("habits/", PublicHabitListApiView.as_view(), name="habit-list"),
    path("habits/<int:pk>/", HabitRetrieveApiView.as_view(), name="habit-detail"),
    path("habits/update/<int:pk>/", HabitUpdateApiView.as_view(), name="habit-update"),
    path("habits/delete/<int:pk>/", HabitDestroyApiView.as_view(), name="habit-delete"),
]
