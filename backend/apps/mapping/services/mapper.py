from apps.mapping.exceptions import MappingValidationError


class RailwayMapper:
    """
    Railway business mapping logic.
    """

    def map(
        self,
        *,
        ai_payload: dict,
        ntes_coaches,
    ):
        raise NotImplementedError

    def _reverse_ntes_order(self, coaches):
        """
        Reverse the NTES coach order to match the pit-line inspection direction.
        """
        return list(reversed(coaches))

    def _resolve_coach_position(
        self,
        coach_position: int,
        reversed_ntes,
    ):
        """
        Resolve an AI coach position to the corresponding NTES coach.
        """
        if coach_position < 1 or coach_position > len(reversed_ntes):
            raise MappingValidationError(f"Invalid coach position: {coach_position}")

        return reversed_ntes[coach_position - 1]
