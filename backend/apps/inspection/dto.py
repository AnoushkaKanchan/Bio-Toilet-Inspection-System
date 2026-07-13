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
    pit_line: str
    train_number: str | None
    status: str
    started_at: str
    defects: int
    inspected_coaches: int
    total_coaches: int


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
