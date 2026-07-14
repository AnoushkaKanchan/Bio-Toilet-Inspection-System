import pytest

from apps.ntes.exceptions import NTESVerificationError
from apps.ntes.services.verification import NTESVerificationService


class Coach:
    def __init__(self, sequence):
        self.coach_sequence = sequence


class RepositoryStub:
    def __init__(self, coaches):
        self._coaches = coaches

    def get_composition(self, *, inspection):
        return self._coaches


@pytest.mark.parametrize(
    "coaches",
    [
        [Coach(0)],
        [Coach(0), Coach(1)],
        [Coach(0), Coach(1), Coach(2), Coach(3)],
    ],
)
def test_verify_valid_composition(coaches):
    service = NTESVerificationService(
        repository=RepositoryStub(coaches),
    )

    result = service.verify(
        inspection=object(),
    )

    assert result == coaches


def test_verify_empty_composition():
    service = NTESVerificationService(
        repository=RepositoryStub([]),
    )

    with pytest.raises(NTESVerificationError):
        service.verify(
            inspection=object(),
        )


def test_verify_sequence_must_start_at_zero():
    service = NTESVerificationService(
        repository=RepositoryStub(
            [Coach(1), Coach(2)],
        ),
    )

    with pytest.raises(NTESVerificationError):
        service.verify(
            inspection=object(),
        )


def test_verify_missing_sequence():
    service = NTESVerificationService(
        repository=RepositoryStub(
            [Coach(0), Coach(1), Coach(3)],
        ),
    )

    with pytest.raises(NTESVerificationError):
        service.verify(
            inspection=object(),
        )


def test_verify_duplicate_sequence():
    service = NTESVerificationService(
        repository=RepositoryStub(
            [Coach(0), Coach(1), Coach(1)],
        ),
    )

    with pytest.raises(NTESVerificationError):
        service.verify(
            inspection=object(),
        )
