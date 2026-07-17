from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True, slots=True)
class TodaySummaryDTO:
    trains_inspected: int
    coaches_inspected: int
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


@dataclass(frozen=True, slots=True)
class TrainInspectionRowDTO:
    train_number: str
    pit_line_number: str
    coaches: int
    tanks: int
    defects: int


@dataclass(frozen=True, slots=True)
class AIObservationDTO:
    total_tanks_inspected: int
    pass_percentage: float
    critical_defects_found: int
    cleaning_required_coaches: int


@dataclass(frozen=True, slots=True)
class DailyReportDTO:
    report_date: date
    generated_at: datetime
    summary: TodaySummaryDTO
    train_rows: list[TrainInspectionRowDTO]
    common_defects: list[CommonDefectDTO]
    ai_observation: AIObservationDTO

@dataclass(frozen=True, slots=True)
class DailyBreakdownDTO:
    day_label: str
    trains: int
    defects: int


@dataclass(frozen=True, slots=True)
class WeeklyTotalsDTO:
    total_trains: int
    total_coaches: int
    total_tanks: int
    average_defects_per_train: float


@dataclass(frozen=True, slots=True)
class WeeklyReportDTO:
    week_start: date
    week_end: date
    generated_at: datetime
    daily_breakdown: list[DailyBreakdownDTO]
    totals: WeeklyTotalsDTO
    top_defects: list[CommonDefectDTO]
    ai_analysis: list[str]


@dataclass(frozen=True, slots=True)
class MonthlyOverviewDTO:
    trains_inspected: int
    coaches_inspected: int
    bio_tanks_inspected: int
    completed: int
    average_defects_per_train: float


@dataclass(frozen=True, slots=True)
class WeekComparisonDTO:
    week_label: str
    trains: int
    defects: int


@dataclass(frozen=True, slots=True)
class PitLinePerformanceDTO:
    pit_line_number: str
    inspections: int
    defects: int
    average_defects_per_inspection: float


@dataclass(frozen=True, slots=True)
class MonthlyReportDTO:
    month_label: str
    generated_at: datetime
    overview: MonthlyOverviewDTO
    weekly_comparison: list[WeekComparisonDTO]
    most_frequent_defects: list[CommonDefectDTO]
    pit_line_performance: list[PitLinePerformanceDTO]
    ai_recommendations: list[str]

