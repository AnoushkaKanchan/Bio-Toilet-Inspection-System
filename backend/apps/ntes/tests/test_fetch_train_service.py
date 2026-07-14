from unittest.mock import Mock

import pytest

from apps.inspection.models import Inspection
from apps.ntes.dto import FetchTrainResponseDTO
from apps.ntes.services import FetchTrainService

pytestmark = pytest.mark.django_db


@pytest.fixture
def inspection():
    inspection = Mock(spec=Inspection)
    inspection.id = "11111111-1111-1111-1111-111111111111"
    return inspection


@pytest.fixture
def inspection_repository(
    inspection,
):
    repository = Mock()
    repository.get.return_value = inspection
    return repository


@pytest.fixture
def synchronization_service():
    service = Mock()
    service.synchronize.return_value = [
        Mock(),
        Mock(),
        Mock(),
    ]
    return service


@pytest.fixture
def ai_repository():
    repository = Mock()
    repository.get_latest_by_inspection.return_value = Mock()
    return repository


@pytest.fixture
def service(
    inspection_repository,
    synchronization_service,
    ai_repository,
):
    return FetchTrainService(
        inspection_repository=inspection_repository,
        synchronization_service=synchronization_service,
        ai_repository=ai_repository,
    )


def test_fetch_returns_dto(
    service,
):
    result = service.fetch(
        inspection_id="11111111-1111-1111-1111-111111111111",
    )

    assert isinstance(
        result,
        FetchTrainResponseDTO,
    )


def test_fetch_success(
    service,
):
    result = service.fetch(
        inspection_id="11111111-1111-1111-1111-111111111111",
    )

    assert result.success is True

    assert result.coaches_synchronized == 3

    assert result.mapping_executed is True


def test_calls_dependencies(
    service,
    inspection_repository,
    synchronization_service,
    ai_repository,
    inspection,
):
    service.fetch(
        inspection_id="11111111-1111-1111-1111-111111111111",
    )

    inspection_repository.get.assert_called_once_with(
        inspection_id="11111111-1111-1111-1111-111111111111",
    )

    synchronization_service.synchronize.assert_called_once_with(
        inspection=inspection,
    )

    ai_repository.get_latest_by_inspection.assert_called_once_with(
        inspection=inspection,
    )


def test_mapping_not_executed(
    inspection_repository,
    synchronization_service,
):
    ai_repository = Mock()
    ai_repository.get_latest_by_inspection.return_value = None

    service = FetchTrainService(
        inspection_repository=inspection_repository,
        synchronization_service=synchronization_service,
        ai_repository=ai_repository,
    )

    result = service.fetch(
        inspection_id="11111111-1111-1111-1111-111111111111",
    )

    assert result.mapping_executed is False


def test_invalid_inspection(
    synchronization_service,
    ai_repository,
):
    repository = Mock()
    repository.get.side_effect = Inspection.DoesNotExist

    service = FetchTrainService(
        inspection_repository=repository,
        synchronization_service=synchronization_service,
        ai_repository=ai_repository,
    )

    with pytest.raises(
        Inspection.DoesNotExist,
    ):
        service.fetch(
            inspection_id="11111111-1111-1111-1111-111111111111",
        )