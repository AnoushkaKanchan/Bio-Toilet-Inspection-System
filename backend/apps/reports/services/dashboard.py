from apps.reports.dto import DashboardSummaryDTO
from apps.reports.repositories import ReportsRepository


class DashboardService:
    def __init__(
        self,
        *,
        repository: ReportsRepository | None = None,
    ) -> None:
        self._repository = repository or ReportsRepository()

    def get_dashboard_summary(
        self,
    ) -> DashboardSummaryDTO:
        return DashboardSummaryDTO(
            today=self._repository.get_today_summary(),
            weekly=self._repository.get_weekly_summary(),
            monthly=self._repository.get_monthly_summary(),
        )
