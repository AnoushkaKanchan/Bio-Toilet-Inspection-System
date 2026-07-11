import pytest

from apps.ntes.dto import NTESCoachDTO
from apps.ntes.models import NTESCoach
from apps.ntes.repositories import NTESCoachRepository


@pytest.fixture
def repository():
    return NTESCoachRepository()


@pytest.fixture
def coach_dtos():
    return [
        NTESCoachDTO(
            coach_sequence=1,
            coach_number="S1",
            coach_type="SL",
        ),
        NTESCoachDTO(
            coach_sequence=2,
            coach_number="S2",
            coach_type="SL",
        ),
    ]


@pytest.mark.django_db
def test_replace_composition_creates_new_records(
    repository,
    inspection,
    coach_dtos,
):
    created = repository.replace_composition(
        inspection=inspection,
        coaches=coach_dtos,
    )

    assert len(created) == 2

    assert (
        NTESCoach.objects.filter(
            inspection=inspection,
        ).count()
        == 2
    )


@pytest.mark.django_db
def test_replace_composition_replaces_existing_records(
    repository,
    inspection,
    coach_dtos,
):
    repository.replace_composition(
        inspection=inspection,
        coaches=coach_dtos,
    )

    replacement = [
        NTESCoachDTO(
            coach_sequence=1,
            coach_number="B1",
            coach_type="3A",
        )
    ]

    repository.replace_composition(
        inspection=inspection,
        coaches=replacement,
    )

    coaches = repository.get_composition(
        inspection=inspection,
    )

    assert len(coaches) == 1
    assert coaches[0].coach_number == "B1"


@pytest.mark.django_db
def test_replace_composition_returns_created_objects(
    repository,
    inspection,
    coach_dtos,
):
    created = repository.replace_composition(
        inspection=inspection,
        coaches=coach_dtos,
    )

    assert all(
        isinstance(
            coach,
            NTESCoach,
        )
        for coach in created
    )


@pytest.mark.django_db
def test_get_composition_returns_ordered_records(
    repository,
    inspection,
):
    repository.replace_composition(
        inspection=inspection,
        coaches=[
            NTESCoachDTO(
                coach_sequence=2,
                coach_number="S2",
                coach_type="SL",
            ),
            NTESCoachDTO(
                coach_sequence=1,
                coach_number="S1",
                coach_type="SL",
            ),
        ],
    )

    coaches = repository.get_composition(
        inspection=inspection,
    )

    assert [coach.coach_sequence for coach in coaches] == [
        1,
        2,
    ]


@pytest.mark.django_db
def test_get_composition_returns_empty_list(
    repository,
    inspection,
):
    coaches = repository.get_composition(
        inspection=inspection,
    )

    assert coaches == []
