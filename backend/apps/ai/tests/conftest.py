import uuid

from django.utils import timezone
import pytest

from apps.inspection.models import Inspection


@pytest.fixture
def inspection(db):
    """
    Creates a valid Inspection for AI persistence tests.

    Update the fields below if your Inspection model
    requires additional mandatory fields.
    """
    return Inspection.objects.create(
        train_number="12951",
        train_name="Rajdhani Exp",
        pit_line_number="P1",
        inspection_time=timezone.now(),
    )

@pytest.fixture
def ai_payload():
    return {
        "inspection_run_id": str(uuid.uuid4()),
        "train_inspection_timestamp": "2026-07-06 14:22:03",
        "video_source": {
            "left_camera": "raw_videos/left.mp4",
            "right_camera": "raw_videos/right.mp4",
        },
        "tanks": [
            {
                "coach_number": 32,
                "tank_id": "L32",
                "synced_tank_id": "R32",
                "camera_side": "LEFT",
                "timestamp_sec": 118.42,
                "pipe_status": "Connected",
                "pipe_support_status": "Absent",
                "surface_status": "Clean",
                "maintenance_status": "Normal",
                "detection_confidence": 0.81,
                "detection_image_path": "cropped.jpg",
            }
        ],
        "summary": {
            "total_coaches_detected": 1,
            "total_bio_tanks": 1,
            "total_maintenance_needed": 0,
            "total_clean_surfaces": 1,
            "total_connected_pipes": 1,
        },
        "status": "COMPLETE",
    }