from unittest.mock import Mock

import pytest

from apps.inspection.services import InspectionWorkflowService


class DummyInspection:
    id = 1


def test_start_invokes_ntes_synchronization():
    inspection = DummyInspection()

    repository = Mock()
    synchronization = Mock()

    expected_coaches = [
        Mock(),
        Mock(),
    ]

    synchronization.synchronize.return_value = expected_coaches

    service = InspectionWorkflowService(
        repository=repository,
        synchronization_service=synchronization,
    )

    result = service.start(
        inspection=inspection,
    )

    synchronization.synchronize.assert_called_once_with(
        inspection=inspection,
    )

    assert result == expected_coaches


@pytest.mark.parametrize(
    "exception",
    [
        RuntimeError("failure"),
    ],
)
def test_start_propagates_synchronization_exception(
    exception,
):
    inspection = DummyInspection()

    repository = Mock()
    synchronization = Mock()

    synchronization.synchronize.side_effect = exception

    service = InspectionWorkflowService(
        repository=repository,
        synchronization_service=synchronization,
    )

    with pytest.raises(type(exception)):
        service.start(
            inspection=inspection,
        )
