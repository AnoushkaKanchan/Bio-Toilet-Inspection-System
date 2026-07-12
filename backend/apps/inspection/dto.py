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
class InspectionListItemDTO:
    inspection_id: str
    train_number: str
    pit_line: str
    status: str
    inspection_time: datetime
    duration_minutes: int
    total_coaches: int
    total_defects: int
