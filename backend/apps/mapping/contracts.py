from dataclasses import dataclass

from apps.ntes.models import NTESCoach


@dataclass(frozen=True)
class ResolvedCoach:
    ai_coach_number: int
    ntes_coach: NTESCoach
