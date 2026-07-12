from datetime import datetime

from apps.inspection.dto import (
    InspectionListItemDTO,
)


def test_inspection_list_item_dto():
    dto = InspectionListItemDTO(
        inspection_id="INS-001",
        train_number="12951",
        pit_line="P1",
        status="COMPLETED",
        inspection_time=datetime.now(),
        duration_minutes=24,
        total_coaches=18,
        total_defects=1,
    )

    assert dto.train_number == "12951"
    assert dto.total_defects == 1
