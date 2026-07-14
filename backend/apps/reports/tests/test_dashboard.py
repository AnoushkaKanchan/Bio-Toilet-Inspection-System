from unittest.mock import Mock

from apps.reports.dto import (
    DashboardSummaryDTO,
    MonthlySummaryDTO,
    TodaySummaryDTO,
    WeeklySummaryDTO,
)
from apps.reports.services import DashboardService


def test_dashboard_summary():
    repository = Mock()

    today = TodaySummaryDTO(
        trains_inspected=2,
        bio_tanks_inspected=8,
        defects_found=3,
        completed=2,
    )

    weekly = WeeklySummaryDTO(
        trains_inspected=10,
        coaches_inspected=40,
        bio_tanks_inspected=160,
        total_defects=15,
    )

    monthly = MonthlySummaryDTO(
        trains_inspected=35,
        coaches_inspected=140,
        bio_tanks_inspected=560,
        total_defects=60,
    )

    repository.get_today_summary.return_value = today
    repository.get_weekly_summary.return_value = weekly
    repository.get_monthly_summary.return_value = monthly

    service = DashboardService(
        repository=repository,
    )

    result = service.get_dashboard_summary()

    assert result == DashboardSummaryDTO(
        today=today,
        weekly=weekly,
        monthly=monthly,
    )

    repository.get_today_summary.assert_called_once_with()
    repository.get_weekly_summary.assert_called_once_with()
    repository.get_monthly_summary.assert_called_once_with()
