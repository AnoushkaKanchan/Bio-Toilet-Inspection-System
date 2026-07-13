from dataclasses import dataclass, field

from apps.ntes.models import NTESCoach


@dataclass(frozen=True)
class ResolvedCoach:
    ai_coach_number: int
    ntes_coach: NTESCoach
    tanks: list[dict] = field(default_factory=list)