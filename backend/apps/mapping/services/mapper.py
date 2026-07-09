from apps.mapping.contracts import ResolvedCoach
from apps.mapping.exceptions import MappingValidationError
from apps.ntes.models import NTESCoach


class RailwayMapper:
    """
    Railway business mapping logic.
    """

    def resolve_coaches(
        self,
        *,
        payload: dict,
        coaches: list[NTESCoach],
    ) -> list[ResolvedCoach]:
        reversed_coaches = self._reverse_ntes_order(
            coaches,
        )

        return self._resolve_ai_coaches(
            payload,
            reversed_coaches,
        )

    def _reverse_ntes_order(
        self,
        coaches: list[NTESCoach],
    ) -> list[NTESCoach]:
        return list(reversed(coaches))

    def _resolve_coach_position(
        self,
        coach_position: int,
        reversed_coaches: list[NTESCoach],
    ) -> NTESCoach:
        if coach_position < 1 or coach_position > len(reversed_coaches):
            raise MappingValidationError(f"Invalid coach position: {coach_position}")

        return reversed_coaches[coach_position - 1]

    def _resolve_ai_coaches(
        self,
        payload: dict,
        reversed_coaches: list[NTESCoach],
    ) -> list[ResolvedCoach]:
        resolved: list[ResolvedCoach] = []

        for tank in payload["tanks"]:
            ai_position = tank["coach_number"]

            coach = self._resolve_coach_position(
                ai_position,
                reversed_coaches,
            )

            resolved.append(
                ResolvedCoach(
                    ai_coach_number=ai_position,
                    ntes_coach=coach,
                )
            )

        return resolved
