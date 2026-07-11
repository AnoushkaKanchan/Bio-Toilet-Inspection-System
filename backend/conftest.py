import pytest
from django.utils import timezone

from apps.inspection.models import Inspection


@pytest.fixture
def inspection():
    return Inspection.objects.create(
        train_number="12951",
        pit_line_number="1",
        inspection_time=timezone.now(),
    )