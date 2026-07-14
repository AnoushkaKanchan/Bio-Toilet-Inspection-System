import uuid
from unittest.mock import patch

import pytest
from rest_framework.test import APIClient

from apps.ntes.dto import FetchTrainResponseDTO

pytestmark = pytest.mark.django_db


@patch("apps.ntes.views.FetchTrainService.fetch")
def test_fetch_train(
    mock_fetch,
    inspection,
):
    mock_fetch.return_value = FetchTrainResponseDTO(
        success=True,
        inspection_id=str(inspection.id),
        coaches_synchronized=22,
        mapping_executed=True,
    )

    client = APIClient()

    response = client.post(
        f"/api/v1/inspections/{inspection.id}/fetch-train/",
    )

    assert response.status_code == 200

    assert response.json() == {
        "success": True,
        "inspection_id": str(inspection.id),
        "coaches_synchronized": 22,
        "mapping_executed": True,
    }


@patch("apps.ntes.views.FetchTrainService.fetch")
def test_invalid_inspection(
    mock_fetch,
):
    from apps.inspection.models import Inspection

    mock_fetch.side_effect = Inspection.DoesNotExist

    client = APIClient()

    response = client.post(
        f"/api/v1/inspections/{uuid.uuid4()}/fetch-train/",
    )

    assert response.status_code == 404

    assert response.json() == {
        "success": False,
        "message": "Inspection not found.",
    }


@patch("apps.ntes.views.FetchTrainService.fetch")
def test_response_schema(
    mock_fetch,
    inspection,
):
    mock_fetch.return_value = FetchTrainResponseDTO(
        success=True,
        inspection_id=str(inspection.id),
        coaches_synchronized=15,
        mapping_executed=False,
    )

    client = APIClient()

    response = client.post(
        f"/api/v1/inspections/{inspection.id}/fetch-train/",
    )

    body = response.json()

    assert set(body.keys()) == {
        "success",
        "inspection_id",
        "coaches_synchronized",
        "mapping_executed",
    }