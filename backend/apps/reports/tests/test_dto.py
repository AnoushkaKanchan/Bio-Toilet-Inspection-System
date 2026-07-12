from dataclasses import FrozenInstanceError

import pytest

from apps.reports.dto import (
    CommonDefectDTO,
    DashboardSummaryDTO,
    MonthlySummaryDTO,
    TodaySummaryDTO,
    WeeklySummaryDTO,
)


def test_today_summary_dto():
    dto = TodaySummaryDTO(
        trains_inspected=9,
        bio_tanks_inspected=72,
        defects_found=21,
        completed=6,
    )

    assert dto.trains_inspected == 9
    assert dto.bio_tanks_inspected == 72
    assert dto.defects_found == 21
    assert dto.completed == 6


def test_dashboard_summary_dto():
    dashboard = DashboardSummaryDTO(
        today=TodaySummaryDTO(1, 2, 3, 4),
        weekly=WeeklySummaryDTO(5, 6, 7, 8),
        monthly=MonthlySummaryDTO(9, 10, 11, 12),
    )

    assert dashboard.today.trains_inspected == 1
    assert dashboard.weekly.coaches_inspected == 6
    assert dashboard.monthly.total_defects == 12


def test_common_defect_dto():
    dto = CommonDefectDTO(
        defect_type="PIPE_NOT_CONNECTED",
        display_name="Pipe Not Connected",
        count=42,
    )

    assert dto.count == 42


def test_dtos_are_immutable():
    dto = TodaySummaryDTO(
        trains_inspected=1,
        bio_tanks_inspected=2,
        defects_found=3,
        completed=4,
    )

    with pytest.raises(FrozenInstanceError):
        dto.completed = 10
