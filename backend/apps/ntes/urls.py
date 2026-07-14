from django.urls import path

from apps.ntes.views import (
    FetchTrainAPIView,
)

urlpatterns = [
    path(
        "inspections/<uuid:inspection_id>/fetch-train/",
        FetchTrainAPIView.as_view(),
    ),
]