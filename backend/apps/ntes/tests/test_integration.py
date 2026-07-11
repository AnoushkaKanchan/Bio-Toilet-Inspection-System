import pytest
from django.db import DatabaseError

from apps.ntes.exceptions import (
    NTESNormalizationError,
    NTESParsingError,
    NTESUnavailableError,
    NTESVerificationError,
)
from apps.ntes.models import NTESCoach
from apps.ntes.repositories import NTESCoachRepository
from apps.ntes.services import SynchronizationService

pytestmark = pytest.mark.django_db


def test_successful_synchronization(
    synchronization_service,
    inspection,
    repository,
):
    coaches = synchronization_service.synchronize(
        inspection=inspection,
    )

    persisted = repository.get_composition(
        inspection=inspection,
    )

    assert len(coaches) == len(persisted)

    for coach in persisted:
        assert coach.inspection_id == inspection.id

    sequences = [coach.coach_sequence for coach in persisted]

    assert sequences == sorted(sequences)
    assert len(sequences) == len(set(sequences))


def test_parser_failure(
    inspection,
    client,
    parser,
    normalizer,
    repository,
    verifier,
):
    client.fetch.return_value = "<html>invalid</html>"

    service = SynchronizationService(
        client=client,
        parser=parser,
        normalizer=normalizer,
        repository=repository,
        verifier=verifier,
    )

    with pytest.raises(
        NTESParsingError,
    ):
        service.synchronize(
            inspection=inspection,
        )

    assert (
        repository.get_composition(
            inspection=inspection,
        )
        == []
    )

    assert (
        NTESCoach.objects.filter(
            inspection=inspection,
        ).count()
        == 0
    )


class FailingNormalizer:
    def normalize(
        self,
        coaches,
    ):
        raise NTESNormalizationError(
            "Normalization failed.",
        )


def test_normalizer_failure(
    inspection,
    client,
    parser,
    repository,
    verifier,
):
    service = SynchronizationService(
        client=client,
        parser=parser,
        normalizer=FailingNormalizer(),
        repository=repository,
        verifier=verifier,
    )

    with pytest.raises(
        NTESNormalizationError,
    ):
        service.synchronize(
            inspection=inspection,
        )

    assert (
        repository.get_composition(
            inspection=inspection,
        )
        == []
    )

    assert (
        NTESCoach.objects.filter(
            inspection=inspection,
        ).count()
        == 0
    )


class FailingRepository(
    NTESCoachRepository,
):
    def replace_composition(
        self,
        **kwargs,
    ):
        raise DatabaseError(
            "Database failure.",
        )


def test_repository_failure(
    inspection,
    client,
    parser,
    normalizer,
    verifier,
):
    repository = FailingRepository()

    service = SynchronizationService(
        client=client,
        parser=parser,
        normalizer=normalizer,
        repository=repository,
        verifier=verifier,
    )

    with pytest.raises(
        DatabaseError,
    ):
        service.synchronize(
            inspection=inspection,
        )

    assert (
        repository.get_composition(
            inspection=inspection,
        )
        == []
    )

    assert (
        NTESCoach.objects.filter(
            inspection=inspection,
        ).count()
        == 0
    )


class FailingVerificationService:
    def verify(
        self,
        *,
        inspection,
    ):
        raise NTESVerificationError(
            "Verification failed.",
        )


def test_verification_failure_rolls_back(
    inspection,
    client,
    parser,
    normalizer,
    repository,
):
    service = SynchronizationService(
        client=client,
        parser=parser,
        normalizer=normalizer,
        repository=repository,
        verifier=FailingVerificationService(),
    )

    with pytest.raises(
        NTESVerificationError,
    ):
        service.synchronize(
            inspection=inspection,
        )

    assert (
        repository.get_composition(
            inspection=inspection,
        )
        == []
    )

    assert (
        NTESCoach.objects.filter(
            inspection=inspection,
        ).count()
        == 0
    )


def test_client_failure(
    inspection,
    client,
    parser,
    normalizer,
    repository,
    verifier,
):
    client.fetch.side_effect = NTESUnavailableError(
        "NTES unavailable.",
    )

    service = SynchronizationService(
        client=client,
        parser=parser,
        normalizer=normalizer,
        repository=repository,
        verifier=verifier,
    )

    with pytest.raises(
        NTESUnavailableError,
    ):
        service.synchronize(
            inspection=inspection,
        )

    assert (
        repository.get_composition(
            inspection=inspection,
        )
        == []
    )

    assert (
        NTESCoach.objects.filter(
            inspection=inspection,
        ).count()
        == 0
    )
