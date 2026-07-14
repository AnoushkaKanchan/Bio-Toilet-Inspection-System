from apps.mapping.contracts import ResolvedCoach
from apps.mapping.services.mapper import RailwayMapper
from apps.ntes.models import NTESCoach
from apps.mapping.enums import TankDefectType


class MappingOrchestrator:
    """
    Coordinates the railway mapping workflow.
    """

    def __init__(self):
        self.mapper = RailwayMapper()

    def execute(
        self,
        *,
        payload: dict,
        coaches: list[NTESCoach],
    ) -> list[ResolvedCoach]:
        return self.mapper.resolve_coaches(
            payload=payload,
            coaches=coaches,
        )

    def translate_defects(
        self,
        tank_payload: dict,
    ) -> list[TankDefectType]:
        return self.mapper.translate_defects(
            tank_payload,
        )