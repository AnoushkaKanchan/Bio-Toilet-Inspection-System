from apps.ntes.dto import (
    NTESCoachDTO,
    RawCoachDTO,
)
from apps.ntes.exceptions import (
    NTESNormalizationError,
)


class NTESNormalizer:
    def normalize(
        self,
        coaches: list[RawCoachDTO],
    ) -> list[NTESCoachDTO]:
        normalized = []

        for coach in coaches:
            self._validate_required_fields(
                coach,
            )

            normalized.append(
                NTESCoachDTO(
                    coach_sequence=self._normalize_sequence(
                        coach.coach_sequence,
                    ),
                    coach_number=self._normalize_coach_number(
                        coach.coach_number,
                    ),
                    coach_type=self._normalize_coach_type(
                        coach.coach_type,
                    ),
                )
            )

        return normalized

    def _validate_required_fields(
        self,
        coach: RawCoachDTO,
    ) -> None:
        if not coach.coach_sequence.strip():
            raise NTESNormalizationError("Coach sequence is required.")

        if not coach.coach_number.strip():
            raise NTESNormalizationError("Coach number is required.")

        if not coach.coach_type.strip():
            raise NTESNormalizationError("Coach type is required.")

    def _normalize_sequence(
        self,
        sequence: str,
    ) -> int:
        value = sequence.strip()

        try:
            return int(value)

        except ValueError as exc:
            raise NTESNormalizationError(
                f"Invalid coach sequence: '{sequence}'."
            ) from exc

    def _normalize_coach_number(
        self,
        coach_number: str,
    ) -> str:
        value = coach_number.strip().upper()

        if not value:
            raise NTESNormalizationError("Coach number cannot be empty.")

        return value

    def _normalize_coach_type(
        self,
        coach_type: str,
    ) -> str:
        value = coach_type.strip().upper()

        if not value:
            raise NTESNormalizationError("Coach type cannot be empty.")

        return value
