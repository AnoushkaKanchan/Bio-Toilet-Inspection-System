from datetime import datetime

from apps.inspection.dto import (
    DefectSummaryDTO,
    InspectionDetailsItemDTO,
    InspectionSummaryDTO,
    MappingStatusDTO,
    TrainInfoDTO,
)


def test_inspection_details_dto():
    dto = InspectionDetailsItemDTO(
        inspection_id="INS-001",
        status="COMPLETED",
        pit_line="P1",
        train=TrainInfoDTO(
            number="12951",
            name="Rajdhani Express",
        ),
        inspection=InspectionSummaryDTO(
            started_at=datetime.now(),
            duration_minutes=24,
            coaches_detected=18,
            total_coaches=18,
            total_defects=1,
        ),
        defect_summary=DefectSummaryDTO(
            pipe_not_connected=0,
            pipe_support_absent=1,
            surface_not_clean=0,
        ),
        mapping=MappingStatusDTO(
            completed=True,
            message="Coach composition verified.",
        ),
    )

    assert dto.train.number == "12951"
    assert dto.inspection.total_defects == 1
    assert dto.mapping.completed is True
