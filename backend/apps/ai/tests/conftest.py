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