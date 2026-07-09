from apps.ai.models import AIResultRaw
from apps.inspection.models import Inspection


class MappingOrchestrator:
    """
    Coordinates the mapping workflow.

    This class contains no railway business rules.
    """

    def __init__(self, inspection: Inspection):
        self.inspection = inspection

    def execute(self):
        """
        Execute the complete mapping workflow.
        """

        raise NotImplementedError(
            "Mapping workflow will be implemented in Mini Phase 5.2."
        )
