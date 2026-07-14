import uuid

import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_post_ai_results(
    inspection,
    ai_payload,
):
    client = APIClient()

    response = client.post(
        "/api/v1/ai/results/",
        {
            "inspection_id": str(
                inspection.id,
            ),
            "payload": ai_payload,
        },
        format="json",
    )

    assert response.status_code == 200

    assert response.json() == {
        "success": True,
        "inspection_id": str(
            inspection.id,
        ),
        "message": "AI results processed successfully.",
    }


def test_invalid_inspection(
    ai_payload,
):
    client = APIClient()

    response = client.post(
        "/api/v1/ai/results/",
        {
            "inspection_id": str(
                uuid.uuid4(),
            ),
            "payload": ai_payload,
        },
        format="json",
    )

    assert response.status_code == 404

    assert response.json() == {
        "success": False,
        "message": "Inspection not found.",
    }


def test_invalid_payload(
    inspection,
    ai_payload,
):
    client = APIClient()

    invalid_payload = dict(
        ai_payload,
    )

    invalid_payload.pop(
        "inspection_run_id",
    )

    response = client.post(
        "/api/v1/ai/results/",
        {
            "inspection_id": str(
                inspection.id,
            ),
            "payload": invalid_payload,
        },
        format="json",
    )

    assert response.status_code == 400

    body = response.json()

    assert body["success"] is False

    assert (
        body["message"]
        == "Missing required field: 'inspection_run_id'."
    )