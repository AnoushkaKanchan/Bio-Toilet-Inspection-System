from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TodaySummaryDTO:
    trains_inspected: int
    bio_tanks_inspected: int
    defects_found: int
    completed: int


@dataclass(frozen=True, slots=True)
class WeeklySummaryDTO:
    trains_inspected: int
    coaches_inspected: int
    bio_tanks_inspected: int
    total_defects: int


@dataclass(frozen=True, slots=True)
class MonthlySummaryDTO:
    trains_inspected: int
    coaches_inspected: int
    bio_tanks_inspected: int
    total_defects: int


@dataclass(frozen=True, slots=True)
class DashboardSummaryDTO:
    today: TodaySummaryDTO
    weekly: WeeklySummaryDTO
    monthly: MonthlySummaryDTO


@dataclass(frozen=True, slots=True)
class CommonDefectDTO:
    defect_type: str
    display_name: str
    count: int
