from dataclasses import dataclass


@dataclass(frozen=True)
class RawCoachDTO:
    """
    Raw coach data extracted directly from the NTES HTML.
    """

    coach_sequence: str
    coach_number: str
    coach_type: str


@dataclass(frozen=True)
class NTESCoachDTO:
    """
    Normalized coach data ready for persistence.
    """

    coach_sequence: int
    coach_number: str
    coach_type: str

@dataclass(slots=True)
class FetchTrainResponseDTO:
    success: bool
    inspection_id: str
    coaches_synchronized: int
    mapping_executed: bool