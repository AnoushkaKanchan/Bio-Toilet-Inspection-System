from django.urls import path

from apps.inspection.views import (
    InspectionListAPIView,
)

urlpatterns = [
    path(
        "inspections/",
        InspectionListAPIView.as_view(),
        name="inspection-list",
    ),
]
