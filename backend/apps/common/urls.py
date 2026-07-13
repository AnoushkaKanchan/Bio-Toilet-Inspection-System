from django.urls import path

from apps.common.views import (
    SettingsAPIView,
)

urlpatterns = [
    path(
        "settings/",
        SettingsAPIView.as_view(),
        name="settings",
    ),
]