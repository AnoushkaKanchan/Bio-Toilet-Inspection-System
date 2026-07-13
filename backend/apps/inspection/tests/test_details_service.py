from apps.inspection.dto import (
    DefectSummaryDTO,
    InspectionDetailsItemDTO,
    InspectionSummaryDTO,
    MappingStatusDTO,
    TrainInfoDTO,
)
from apps.inspection.services import InspectionDetailsService
import pytest

pytestmark = pytest.mark.django_db

def test_get_inspection_details(
    inspection,
):
    service = InspectionDetailsService()

    details = service.get_details(
        inspection_id=inspection.id,
    )

    assert isinstance(
        details,
        InspectionDetailsItemDTO,
    )

    assert isinstance(
        details.train,
        TrainInfoDTO,
    )

    assert isinstance(
        details.inspection,
        InspectionSummaryDTO,
    )

    assert isinstance(
        details.defect_summary,
        DefectSummaryDTO,
    )

    assert isinstance(
        details.mapping,
        MappingStatusDTO,
    )

    assert details.train.number == inspection.train_number

    assert details.train.name == inspection.train_name

    assert (
        details.inspection.total_coaches
        == inspection.total_coaches
    )

    assert (
        details.inspection.total_defects
        == inspection.total_defected_tanks
    )

    assert (
        details.mapping.completed
        == (inspection.status == "COMPLETED")
    )

def test_train_information(
    inspection,
):
    service = InspectionDetailsService()

    result = service.get_details(
        inspection_id=inspection.id,
    )

    assert (
        result.train.number
        == inspection.train_number
    )

    assert (
        result.train.name
        == inspection.train_name
    )

def test_inspection_summary(
    inspection,
):
    service = InspectionDetailsService()

    result = service.get_details(
        inspection_id=inspection.id,
    )

    assert (
        result.inspection.started_at
        == inspection.inspection_time
    )

    assert (
        result.inspection.total_coaches
        == inspection.total_coaches
    )

    assert (
        result.inspection.total_defects
        == inspection.total_defected_tanks
    )

    assert (
        result.inspection.duration_minutes
        >= 0
    )

def test_default_defect_summary(
    inspection,
):
    service = InspectionDetailsService()

    result = service.get_details(
        inspection_id=inspection.id,
    )

    assert (
        result.defect_summary.pipe_not_connected
        == 0
    )

    assert (
        result.defect_summary.pipe_support_absent
        == 0
    )

    assert (
        result.defect_summary.surface_not_clean
        == 0
    )

def test_mapping_status(
    inspection,
):
    service = InspectionDetailsService()

    result = service.get_details(
        inspection_id=inspection.id,
    )

    assert (
        result.mapping.completed
        is False
    )

    assert (
        inspection.train_number
        in result.mapping.message
    )