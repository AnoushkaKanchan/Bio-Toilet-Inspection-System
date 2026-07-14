from apps.inspection.models import Inspection
from apps.ntes.exceptions import NTESVerificationError
from apps.ntes.models import NTESCoach
from apps.ntes.repositories import NTESCoachRepository


class NTESVerificationService:
    def __init__(
        self,
        repository: NTESCoachRepository | None = None,
    ) -> None:
        self._repository = repository or NTESCoachRepository()

    def verify(
        self,
        *,
        inspection: Inspection,
    ) -> list[NTESCoach]:
        coaches = self._load_composition(
            inspection=inspection,
        )

        self._verify_exists(
            coaches,
        )

        self._verify_sequences(
            coaches,
        )

        return coaches

    def _load_composition(
        self,
        *,
        inspection: Inspection,
    ) -> list[NTESCoach]:
        return self._repository.get_composition(
            inspection=inspection,
        )

    def _verify_exists(
        self,
        coaches: list[NTESCoach],
    ) -> None:
        if not coaches:
            raise NTESVerificationError("No NTES coach composition found.")

    def _verify_sequences(
        self,
        coaches: list[NTESCoach],
    ) -> None:
        sequences = [coach.coach_sequence for coach in coaches]

        if sequences[0] != 0:
            raise NTESVerificationError("Coach sequence must start at 0.")

        if len(sequences) != len(set(sequences)):
            raise NTESVerificationError("Duplicate coach sequence detected.")

        # Repository guarantees ordering by coach_sequence.
        expected = list(
            range(
                0,
                len(sequences),
            )
        )

        if sequences != expected:
            raise NTESVerificationError("Coach sequence is not continuous.")
