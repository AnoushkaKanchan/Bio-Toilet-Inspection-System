import uuid

from django.urls import reverse
import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_get_details_contains_nested_sections(
    inspection,
):
    client = APIClient()

    response = client.get(
        reverse(
            "inspection-details",
            kwargs={"inspection_id": inspection.id},
        )
    )

    assert response.status_code == 200

    body = response.json()

    # Ensures the structural layout contract remains unflattened
    assert set(body.keys()) == {
        "inspection_id",
        "status",
        "pit_line",
        "train",
        "inspection",
        "defect_summary",
        "mapping",
    }


def test_details_endpoint_returns_exact_contract_values(
    inspection,
):
    client = APIClient()

    response = client.get(
        f"/api/v1/inspection/{inspection.id}/",
    )

    assert response.status_code == 200

    body = response.json()

    # Root Level Values
    assert body["inspection_id"] == str(inspection.id)
    assert body["status"] == inspection.status
    assert body["pit_line"] == inspection.pit_line_number

    # Train Information Section
    assert body["train"]["number"] == inspection.train_number
    assert body["train"]["name"] == inspection.train_name

    # Inspection Aggregates Section
    assert body["inspection"]["total_coaches"] == inspection.total_coaches
    assert body["inspection"]["total_defects"] == inspection.total_defected_tanks

    assert "started_at" in body["inspection"]
    assert body["inspection"]["duration_minutes"] >= 0
    assert (body["inspection"]["coaches_detected"]== inspection.total_coaches)

    # Defect Summary Section (Zero-state validation for this fixture context)
    assert body["defect_summary"] == {
        "pipe_not_connected": 0,
        "pipe_support_absent": 0,
        "surface_not_clean": 0,
    }

    # Mapping Metadata Section
    assert body["mapping"]["completed"] is False
    assert inspection.train_number in body["mapping"]["message"]


def test_get_details_endpoint_returns_404_not_found():
    client = APIClient()

    response = client.get(
        f"/api/v1/inspection/{uuid.uuid4()}/",
    )

    assert response.status_code == 404

    body = response.json()
    
    # Exact verification of the error schema payload
    assert body["success"] is False
    assert body["message"] == "Inspection not found."