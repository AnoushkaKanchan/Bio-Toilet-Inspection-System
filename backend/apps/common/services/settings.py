from apps.common.dto import (
    AboutDTO,
    PreferencesDTO,
    SettingsDTO,
    SupportDTO,
)
from apps.common.repositories import (
    SettingsRepository,
)
from apps.common.services.health import (
    HealthService,
)


class SettingsService:

    def __init__(
        self,
        *,
        repository: SettingsRepository | None = None,
        health_service: HealthService | None = None,
    ) -> None:

        self._repository = (
            repository
            or SettingsRepository()
        )

        self._health_service = (
            health_service
            or HealthService(
                repository=self._repository,
            )
        )

    def get_settings(
        self,
    ) -> SettingsDTO:

        preferences = PreferencesDTO(
            auto_refresh=self._repository.get_auto_refresh(),
        )

        about = AboutDTO(
            application_name=self._repository.get_application_name(),
            version=self._repository.get_version(),
            technical_support=SupportDTO(
                email=self._repository.get_support_email(),
            ),
        )

        return SettingsDTO(
            system_status=self._health_service.get_system_status(),
            preferences=preferences,
            about=about,
        )