import pytest

from apps.inspection.dto import CoachInspectionReportDTO
from apps.inspection.services import CoachInspectionReportService

pytestmark = pytest.mark.django_db

def test_get_report_returns_dto(
    inspection,
    coach,
):
    service = CoachInspectionReportService()

    report = service.get_report(
        inspection_id=inspection.id,
        coach_id=coach.id,
    )

    assert isinstance(
        report,
        CoachInspectionReportDTO,
    )

def test_navigation_fields_exist(
    inspection,
    coach,
):
    service = CoachInspectionReportService()

    report = service.get_report(
        inspection_id=inspection.id,
        coach_id=coach.id,
    )

    assert hasattr(
        report.navigation,
        "previous",
    )

    assert hasattr(
        report.navigation,
        "next",
    )

def test_empty_findings(
    inspection,
    coach,
):
    service = CoachInspectionReportService()

    report = service.get_report(
        inspection_id=inspection.id,
        coach_id=coach.id,
    )

    assert report.findings == []

def test_default_remarks(
    inspection,
    coach,
):
    service = CoachInspectionReportService()

    report = service.get_report(
        inspection_id=inspection.id,
        coach_id=coach.id,
    )

    assert report.remarks == "No issues detected."