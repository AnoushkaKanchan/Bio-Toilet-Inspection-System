from unittest.mock import Mock

import pytest

from apps.reports.dto import (
    MonthlySummaryDTO,
    TodaySummaryDTO,
    WeeklySummaryDTO,
)
from apps.reports.services import ExportService


@pytest.fixture
def repository():
    return Mock()


@pytest.fixture
def service(repository):
    return ExportService(
        repository=repository,
    )


def test_export_daily(
    service,
    repository,
):
    summary = TodaySummaryDTO(
        trains_inspected=1,
        bio_tanks_inspected=2,
        defects_found=3,
        completed=1,
    )

    repository.get_today_summary.return_value = summary

    pdf = service.export(report_type="daily")

    assert isinstance(pdf, bytes)
    assert len(pdf) > 0

    repository.get_today_summary.assert_called_once_with()


def test_export_weekly(
    service,
    repository,
):
    summary = WeeklySummaryDTO(
        trains_inspected=10,
        coaches_inspected=20,
        bio_tanks_inspected=80,
        total_defects=15,
    )

    repository.get_weekly_summary.return_value = summary

    pdf = service.export(report_type="weekly")

    assert isinstance(pdf, bytes)
    assert len(pdf) > 0

    repository.get_weekly_summary.assert_called_once_with()


def test_export_monthly(
    service,
    repository,
):
    summary = MonthlySummaryDTO(
        trains_inspected=40,
        coaches_inspected=160,
        bio_tanks_inspected=640,
        total_defects=100,
    )

    repository.get_monthly_summary.return_value = summary

    pdf = service.export(report_type="monthly")

    assert isinstance(pdf, bytes)
    assert len(pdf) > 0

    repository.get_monthly_summary.assert_called_once_with()


def test_invalid_report_type(
    service,
):
    with pytest.raises(ValueError):
        service.export(
            report_type="yearly",
        )
