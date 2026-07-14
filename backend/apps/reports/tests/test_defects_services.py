from unittest.mock import Mock

from apps.reports.dto import CommonDefectDTO
from apps.reports.services import CommonDefectsService


def test_get_common_defects():
    repository = Mock()

    expected = [
        CommonDefectDTO(
            defect_type="PIPE_NOT_CONNECTED",
            display_name="Pipe Not Connected",
            count=12,
        ),
        CommonDefectDTO(
            defect_type="SURFACE_NOT_CLEAN",
            display_name="Surface Not Clean",
            count=5,
        ),
    ]

    repository.get_common_defects.return_value = expected

    service = CommonDefectsService(
        repository=repository,
    )

    result = service.get_common_defects(
        limit=5,
    )

    assert result == expected

    repository.get_common_defects.assert_called_once_with(
        limit=5,
    )


def test_default_limit():
    repository = Mock()
    repository.get_common_defects.return_value = []

    service = CommonDefectsService(
        repository=repository,
    )

    assert service.get_common_defects() == []

    repository.get_common_defects.assert_called_once_with(
        limit=10,
    )
