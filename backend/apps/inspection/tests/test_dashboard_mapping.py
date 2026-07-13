import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_train_mapping_endpoint(
    inspection,
):
    client = APIClient()

    response = client.get(
        f"/api/v1/dashboard/train-mapping/{inspection.id}/",
    )

    assert response.status_code == 200

    body = response.json()

    assert "inspection_id" in body
    assert "train_number" in body
    assert "coaches" in body
