from unittest.mock import Mock

import pytest

from apps.ai.dto import AIAcknowledgementDTO
from apps.ai.services.results import AIResultService
from apps.inspection.models import Inspection

pytestmark = pytest.mark.django_db


@pytest.fixture
def inspection_mock():
    inspection = Mock(spec=Inspection)
    inspection.id = "11111111-1111-1111-1111-111111111111"
    return inspection


@pytest.fixture
def validator():
    return Mock()


@pytest.fixture
def persistence():
    return Mock()


@pytest.fixture
def inspection_repository(
    inspection_mock,
):
    repository = Mock()
    repository.get.return_value = inspection_mock
    return repository


@pytest.fixture
def service(
    validator,
    persistence,
    inspection_repository,
):
    return AIResultService(
        validator=validator,
        persistence_service=persistence,
        inspection_repository=inspection_repository,
    )


def test_process_returns_acknowledgement(
    service,
    ai_payload,
):
    result = service.process(
        inspection_id="11111111-1111-1111-1111-111111111111",
        payload=ai_payload,
    )

    assert isinstance(
        result,
        AIAcknowledgementDTO,
    )


def test_process_calls_dependencies(
    service,
    validator,
    persistence,
    inspection_repository,
    inspection_mock,
    ai_payload,
):
    service.process(
        inspection_id="11111111-1111-1111-1111-111111111111",
        payload=ai_payload,
    )

    validator.validate.assert_called_once_with(
        payload=ai_payload,
    )

    inspection_repository.get.assert_called_once_with(
        inspection_id="11111111-1111-1111-1111-111111111111",
    )

    persistence.persist.assert_called_once_with(
        inspection=inspection_mock,
        payload=ai_payload,
    )


def test_process_returns_success(
    service,
    ai_payload,
):
    result = service.process(
        inspection_id="11111111-1111-1111-1111-111111111111",
        payload=ai_payload,
    )

    assert result.success is True

    assert (
        result.message
        == "AI results processed successfully."
    )


def test_invalid_inspection(
    validator,
    persistence,
    ai_payload,
):
    inspection_repository = Mock()

    inspection_repository.get.side_effect = (
        Inspection.DoesNotExist
    )

    service = AIResultService(
        validator=validator,
        persistence_service=persistence,
        inspection_repository=inspection_repository,
    )

    with pytest.raises(
        Inspection.DoesNotExist,
    ):
        service.process(
            inspection_id="11111111-1111-1111-1111-111111111111",
            payload=ai_payload,
        )