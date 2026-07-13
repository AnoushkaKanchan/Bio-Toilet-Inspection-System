from django.urls import path

from apps.inspection.views import (
    InspectionDetailsAPIView,
    InspectionListAPIView,
)

urlpatterns = [
    path(
        "inspections/",
        InspectionListAPIView.as_view(),
        name="inspection-list",
    ),
    path(
        "inspection/<uuid:inspection_id>/",
        InspectionDetailsAPIView.as_view(),
        name="inspection-details",
    ),
]
