import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_coach_list_integration(
    inspection,
):
    client = APIClient()

    response = client.get(
        f"/api/v1/inspection/{inspection.id}/coaches/",
    )

    assert response.status_code == 200

    body = response.json()

    assert body["inspection_id"] == str(
        inspection.id,
    )

    assert isinstance(
        body["coaches"],
        list,
    )


def test_coach_list_search(
    inspection,
):
    client = APIClient()

    response = client.get(
        f"/api/v1/inspection/{inspection.id}/coaches/?search=B1",
    )

    assert response.status_code == 200


def test_coach_list_filter_clean(
    inspection,
):
    client = APIClient()

    response = client.get(
        f"/api/v1/inspection/{inspection.id}/coaches/?filter=CLEAN",
    )

    assert response.status_code == 200


def test_coach_list_filter_defect(
    inspection,
):
    client = APIClient()

    response = client.get(
        f"/api/v1/inspection/{inspection.id}/coaches/?filter=DEFECT",
    )

    assert response.status_code == 200