from django.urls import path

from apps.inspection.views import (
    CoachInspectionImagesAPIView,
    CoachInspectionReportAPIView,
    CoachListAPIView,
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
    path(
        "inspection/<uuid:inspection_id>/coaches/",
        CoachListAPIView.as_view(),
        name="coach-list",
    ),
    path(
        "inspection/<uuid:inspection_id>/coaches/<uuid:coach_id>/",
        CoachInspectionReportAPIView.as_view(),
        name="coach-details",
    ),
    path(
    "inspections/<uuid:inspection_id>/coaches/<uuid:coach_id>/images/",
    CoachInspectionImagesAPIView.as_view(),
    ),
]