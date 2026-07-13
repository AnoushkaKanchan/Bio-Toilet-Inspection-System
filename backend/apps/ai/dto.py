from dataclasses import dataclass


@dataclass(frozen=True)
class AIAcknowledgementDTO:
    success: bool
    inspection_id: str
    message: str