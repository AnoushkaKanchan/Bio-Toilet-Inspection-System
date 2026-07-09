from dataclasses import dataclass


@dataclass(frozen=True)
class InspectionStatistics:
    total_coaches: int
    total_tanks: int
    total_defected_tanks: int

    @property
    def healthy_tanks(self) -> int:
        return self.total_tanks - self.total_defected_tanks
