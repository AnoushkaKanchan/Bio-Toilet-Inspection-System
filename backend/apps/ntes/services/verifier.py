from apps.inspection.models import Inspection
from apps.ntes.exceptions import NTESVerificationError
from apps.ntes.models import NTESCoach


class NTESVerifier:
    """
    Verifies that the validated AI payload can be matched
    against the current NTES coach composition.
    """

    def verify(
        self,
        inspection: Inspection,
        payload: dict,
    ) -> None:
        self._validate_inspection(inspection)

        coaches = self._load_coach_composition(
            inspection,
        )

        self._verify_ai_coaches(
            payload,
            coaches,
        )

    def _validate_inspection(
        self,
        inspection: Inspection,
    ) -> None:
        if inspection is None:
            raise NTESVerificationError("Inspection does not exist.")

    def _load_coach_composition(
        self,
        inspection: Inspection,
    ) -> list[NTESCoach]:
        coaches = list(
            NTESCoach.objects.filter(
                inspection=inspection,
            ).order_by("coach_sequence")
        )

        if not coaches:
            raise NTESVerificationError("No NTES coach composition found.")

        return coaches

    def _verify_ai_coaches(
        self,
        payload: dict,
        coaches: list[NTESCoach],
    ) -> None:
        max_position = len(coaches)

        for tank in payload["tanks"]:
            coach_position = tank["coach_number"]

            if coach_position < 1 or coach_position > max_position:
                raise NTESVerificationError(
                    f"Invalid AI coach_number: {coach_position}"
                )
