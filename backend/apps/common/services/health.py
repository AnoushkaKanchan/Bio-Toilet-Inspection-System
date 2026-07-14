from apps.common.dto import (
    ServiceStatusDTO,
    SystemStatusDTO,
)
from apps.common.health_repository import (
    HealthRepository,
)


class HealthService:

    def __init__(
        self,
        *,
        repository: HealthRepository | None = None,
    ):
        self._repository = (
            repository
            or HealthRepository()
        )

    def get_system_status(
        self,
    ) -> SystemStatusDTO:

        database_status = (
            "ONLINE"
            if self._repository.is_database_online()
            else "OFFLINE"
        )

        backend_status = (
            "ONLINE"
            if database_status == "ONLINE"
            else "DEGRADED"
        )
        
        services = [
            ServiceStatusDTO(
                name="AI Inference Engine",
                status="UNKNOWN",
            ),
            ServiceStatusDTO(
                name="Camera Network",
                status="UNKNOWN",
            ),
            ServiceStatusDTO(
                name="Backend Connection",
                status=backend_status,
            ),
            ServiceStatusDTO(
                name="Database",
                status=database_status,
            ),
        ]

        overall = (
            "ONLINE"
            if database_status == "ONLINE"
            else "DEGRADED"
        )

        return SystemStatusDTO(
            overall=overall,
            last_updated=self._repository.get_timestamp(),
            services=services,
        )