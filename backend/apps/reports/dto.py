from dataclasses import dataclass

from apps.mapping.enums import (
    Camera,
    CoachInspectionStatus,
    TankDefectType,
)


@dataclass(frozen=True)
class InspectionOverview:
    train_number: str
    pitline_number: str
    inspection_timestamp: str
    processing_timestamp: str


@dataclass(frozen=True)
class InspectionSummary:
    total_coaches: int
    total_tanks: int
    total_defected_tanks: int

    @property
    def healthy_tanks(self) -> int:
        return self.total_tanks - self.total_defected_tanks


@dataclass(frozen=True)
class TankDefectResult:
    defect_type: TankDefectType
    confidence: float


@dataclass(frozen=True)
class TankResult:
    tank_identifier: str
    camera: Camera
    timestamp_seconds: float
    confidence: float
    evidence_image_path: str | None
    defects: list[TankDefectResult]


@dataclass(frozen=True)
class CoachResult:
    coach_number: str
    inspection_sequence: int
    status: CoachInspectionStatus
    tanks: list[TankResult]


@dataclass(frozen=True)
class InspectionResult:
    overview: InspectionOverview
    summary: InspectionSummary
    coaches: list[CoachResult]
