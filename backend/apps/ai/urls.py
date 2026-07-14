from django.urls import path

from apps.ai.views import (
    AIResultAPIView,
)

urlpatterns = [
    path(
        "ai/results/",
        AIResultAPIView.as_view(),
        name="ai-results",
    ),
]