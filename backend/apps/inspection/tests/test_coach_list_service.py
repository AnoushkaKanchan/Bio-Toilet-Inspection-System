import pytest

from apps.inspection.dto import (
    CoachListItemDTO,
    CoachListResponseDTO,
)
from apps.inspection.services import CoachListService

pytestmark = pytest.mark.django_db


def test_get_coaches_returns_response(
    inspection,
):
    service = CoachListService()

    response = service.get_coaches(
        inspection_id=inspection.id,
    )

    assert isinstance(
        response,
        CoachListResponseDTO,
    )

    assert response.train_number == inspection.train_number
    assert response.train_name == inspection.train_name


def test_invalid_filter(
    inspection,
):
    service = CoachListService()

    with pytest.raises(ValueError):
        service.get_coaches(
            inspection_id=inspection.id,
            filter_by="INVALID",
        )


def test_search_returns_empty(
    inspection,
):
    service = CoachListService()

    response = service.get_coaches(
        inspection_id=inspection.id,
        search="XYZ",
    )

    assert response.coaches == []