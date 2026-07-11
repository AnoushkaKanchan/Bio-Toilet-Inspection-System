import pytest

from apps.ntes.dto import (
    NTESCoachDTO,
    RawCoachDTO,
)
from apps.ntes.exceptions import (
    NTESNormalizationError,
)
from apps.ntes.normalizer import (
    NTESNormalizer,
)


@pytest.fixture
def normalizer():
    return NTESNormalizer()


def test_normalize_single_coach(
    normalizer,
):
    raw = [
        RawCoachDTO(
            coach_sequence=" 12 ",
            coach_number=" s3 ",
            coach_type=" sl ",
        )
    ]

    result = normalizer.normalize(
        raw,
    )

    assert result == [
        NTESCoachDTO(
            coach_sequence=12,
            coach_number="S3",
            coach_type="SL",
        )
    ]


def test_invalid_sequence(
    normalizer,
):
    raw = [
        RawCoachDTO(
            coach_sequence="ABC",
            coach_number="S1",
            coach_type="SL",
        )
    ]

    with pytest.raises(
        NTESNormalizationError,
    ):
        normalizer.normalize(
            raw,
        )


def test_empty_coach_number(
    normalizer,
):
    raw = [
        RawCoachDTO(
            coach_sequence="1",
            coach_number="",
            coach_type="SL",
        )
    ]

    with pytest.raises(
        NTESNormalizationError,
    ):
        normalizer.normalize(
            raw,
        )


def test_empty_coach_type(
    normalizer,
):
    raw = [
        RawCoachDTO(
            coach_sequence="1",
            coach_number="S1",
            coach_type="",
        )
    ]

    with pytest.raises(
        NTESNormalizationError,
    ):
        normalizer.normalize(
            raw,
        )


def test_multiple_coaches(
    normalizer,
):
    raw = [
        RawCoachDTO(
            coach_sequence="1",
            coach_number=" s1 ",
            coach_type=" sl ",
        ),
        RawCoachDTO(
            coach_sequence="2",
            coach_number=" b1 ",
            coach_type=" 3A ",
        ),
    ]

    result = normalizer.normalize(
        raw,
    )

    assert len(result) == 2

    assert result[0].coach_number == "S1"
    assert result[1].coach_number == "B1"
