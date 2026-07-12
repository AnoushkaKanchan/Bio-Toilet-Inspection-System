from django.urls import path

from apps.reports.views import (
    CommonDefectsView,
    DashboardView,
    ExportView,
)

urlpatterns = [
    path(
        "dashboard/",
        DashboardView.as_view(),
        name="reports-dashboard",
    ),
    path(
        "common-defects/",
        CommonDefectsView.as_view(),
        name="reports-common-defects",
    ),
    path(
        "export/",
        ExportView.as_view(),
        name="reports-export",
    ),
]
