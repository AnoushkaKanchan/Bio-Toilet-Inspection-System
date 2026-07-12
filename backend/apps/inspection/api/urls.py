from django.urls import path

from .views import (
    DashboardSummaryView,
    LivePitLineView,
    OperationsStatusView,
    RecentActivityView,
    TrainMappingView,
)

urlpatterns = [
    path(
        "summary/",
        DashboardSummaryView.as_view(),
        name="dashboard-summary",
    ),
    path(
        "live-pitlines/",
        LivePitLineView.as_view(),
        name="dashboard-live-pitlines",
    ),
    path(
        "status/",
        OperationsStatusView.as_view(),
        name="dashboard-status",
    ),
    path(
        "recent-activity/",
        RecentActivityView.as_view(),
        name="dashboard-recent-activity",
    ),
    path(
        "train-mapping/<uuid:inspection_id>/",
        TrainMappingView.as_view(),
        name="dashboard-train-mapping",
    ),
]
