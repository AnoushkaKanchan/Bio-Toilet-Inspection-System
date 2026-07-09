from dataclasses import dataclass


@dataclass(frozen=True)
class CoachMappingResult:
    coach_position: int  # AI position after pit-line orientation
    coach_sequence: int  # Original NTES sequence
    coach_number: str  # NTES coach number
