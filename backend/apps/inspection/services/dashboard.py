from apps.reports.services.dashboard import DashboardService as ReportsDashboardService


class DashboardService:
    def __init__(
        self,
        reports_dashboard_service: ReportsDashboardService | None = None,
    ) -> None:
        self._reports_dashboard_service = (
            reports_dashboard_service
            or ReportsDashboardService()
        )

    def get_summary(self) -> dict:
        dashboard = self._reports_dashboard_service.get_dashboard_summary()

        return {
            "today": {
                "trains_inspected": dashboard.today.trains_inspected,
                "bio_tanks_inspected": dashboard.today.bio_tanks_inspected,
                "defects_found": dashboard.today.defects_found,
                "completed_inspections": dashboard.today.completed,
            }
        }