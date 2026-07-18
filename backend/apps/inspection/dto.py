from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class InspectionStatistics:
    total_coaches: int
    total_tanks: int
    total_defected_tanks: int

    @property
    def healthy_tanks(self) -> int:
        return self.total_tanks - self.total_defected_tanks


@dataclass(frozen=True)
class LivePitLineDTO:
    inspection_id: str
    pit_line: str
    train_number: str | None
    status: str
    started_at: str
    duration_minutes: int
    defects: int
    inspected_coaches: int
    total_coaches: int
    defect_summary: DefectSummaryDTO

@dataclass(frozen=True)
class RecentActivityDTO:
    inspection_id: str
    train_number: str
    pit_line: str
    status: str
    timestamp: str


@dataclass(frozen=True)
class TrainInfoDTO:
    number: str
    name: str | None
    coaches_synchronized: int


# apps/inspection/dto.py
@dataclass(frozen=True)
class InspectionSummaryDTO:
    started_at: datetime
    duration_minutes: int
    coaches_detected: int
    total_coaches: int
    total_defects: int


@dataclass(frozen=True)
class DefectSummaryDTO:
    pipe_not_connected: int
    pipe_support_absent: int
    surface_not_clean: int


@dataclass(frozen=True)
class MappingStatusDTO:
    completed: bool
    message: str
    train: TrainInfoDTO


@dataclass(frozen=True)
class InspectionDetailsItemDTO:
    inspection_id: str
    status: str
    pit_line: str
    train: TrainInfoDTO
    inspection: InspectionSummaryDTO
    defect_summary: DefectSummaryDTO
    mapping: MappingStatusDTO


@dataclass(frozen=True)
class InspectionListItemDTO:
    inspection_id: str
    train_number: str
    train_name: str | None
    inspection_time: datetime
    pit_line: str
    status: str
    issue_count: int


@dataclass(frozen=True)
class CoachListItemDTO:
    coach_id: str
    inspection_sequence: int
    coach_number: str
    coach_type: str
    status: str
    left_side: str
    right_side: str
    confidence: float
    tank_count: int
    defect_count: int


@dataclass(frozen=True)
class CoachListResponseDTO:
    inspection_id: str
    train_number: str
    train_name: str | None
    coaches: list[CoachListItemDTO]

@dataclass(frozen=True)
class CoachInfoDTO:
    number: str
    type: str
    status: str

@dataclass(frozen=True)
class CoachInspectionSummaryDTO:
    left_status: str
    right_status: str
    overall_confidence: int

@dataclass(frozen=True)
class HealthDiagramDTO:
    front_left: str
    front_right: str
    rear_left: str
    rear_right: str
    bio_tank: str

@dataclass(frozen=True)
class FindingDTO:
    title: str
    description: str
    confidence: int

@dataclass(frozen=True)
class NavigationDTO:
    previous: str | None
    next: str | None

@dataclass(frozen=True)
class CoachInspectionReportDTO:
    coach: CoachInfoDTO
    inspection: CoachInspectionSummaryDTO
    health_diagram: HealthDiagramDTO
    findings: list[FindingDTO]
    maintenance: list[str]
    remarks: str
    navigation: NavigationDTO