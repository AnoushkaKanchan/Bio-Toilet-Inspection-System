from unittest.mock import Mock

import pytest

from apps.inspection.services import InspectionWorkflowService
from apps.ntes.exceptions import NTESUnavailableError
from apps.ntes.models import NTESCoach

pytestmark = pytest.mark.django_db


def test_workflow_persists_ntes_composition(
    inspection,
    workflow_service,
):
    coaches = workflow_service.start(
        inspection=inspection,
    )

    persisted = NTESCoach.objects.filter(
        inspection=inspection,
    ).order_by(
        "coach_sequence",
    )

    assert persisted.exists()

    assert len(coaches) == persisted.count()

    for coach in persisted:
        assert coach.inspection == inspection

    persisted_sequences = [coach.coach_sequence for coach in persisted]

    returned_sequences = [coach.coach_sequence for coach in coaches]

    assert persisted_sequences == returned_sequences


def test_workflow_calls_ntes_once(
    inspection,
    workflow_service,
    client,
):
    workflow_service.start(
        inspection=inspection,
    )

    client.fetch.assert_called_once_with(
        train_number=inspection.train_number,
    )


def test_workflow_propagates_ntes_failure(
    inspection,
):
    synchronization = Mock()

    synchronization.synchronize.side_effect = NTESUnavailableError(
        "NTES unavailable.",
    )

    workflow = InspectionWorkflowService(
        synchronization_service=synchronization,
    )

    with pytest.raises(
        NTESUnavailableError,
    ):
        workflow.start(
            inspection=inspection,
        )
