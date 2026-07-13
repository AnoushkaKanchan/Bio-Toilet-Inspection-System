from apps.common.dto import (
    ServiceStatusDTO,
    SystemStatusDTO,
)
from apps.common.repositories import (
    SettingsRepository,
)


class HealthService:

    def __init__(
        self,
        *,
        repository: SettingsRepository | None = None,
    ) -> None:
        self._repository = (
            repository
            or SettingsRepository()
        )

    def get_system_status(
        self,
    ) -> SystemStatusDTO:

        services = [
            ServiceStatusDTO(
                name="AI Inference Engine",
                status="ONLINE",
            ),
            ServiceStatusDTO(
                name="Camera Network",
                status="ONLINE",
            ),
            ServiceStatusDTO(
                name="Backend Connection",
                status="ONLINE",
            ),
        ]

        return SystemStatusDTO(
            overall="ONLINE",
            last_updated=self._repository.get_last_updated(),
            services=services,
        )