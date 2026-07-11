import pytest

from apps.ntes.models import NTESCoach


@pytest.mark.django_db
def test_successful_synchronization(
    synchronization_service,
    inspection,
):
    coaches = synchronization_service.synchronize(
        inspection=inspection,
    )

    persisted = NTESCoach.objects.filter(
        inspection=inspection,
    ).order_by("coach_sequence")

    assert persisted.exists()
    assert len(coaches) == persisted.count()

    for coach in persisted:
        assert coach.inspection_id == inspection.id

    sequences = [
        coach.coach_sequence
        for coach in persisted
    ]

    assert sequences == sorted(sequences)
    assert len(sequences) == len(set(sequences))