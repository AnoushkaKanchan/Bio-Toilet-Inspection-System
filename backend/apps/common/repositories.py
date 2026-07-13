from django.utils import timezone


class SettingsRepository:

    APPLICATION_NAME = (
        "AI Railway Bio-Toilet Inspection System"
    )

    APPLICATION_VERSION = (
        "1.0.0 Prototype"
    )

    SUPPORT_EMAIL = (
        "support@example.com"
    )

    AUTO_REFRESH = True

    def get_application_name(
        self,
    ) -> str:
        return self.APPLICATION_NAME

    def get_version(
        self,
    ) -> str:
        return self.APPLICATION_VERSION

    def get_support_email(
        self,
    ) -> str:
        return self.SUPPORT_EMAIL

    def get_auto_refresh(
        self,
    ) -> bool:
        return self.AUTO_REFRESH

    def get_last_updated(
        self,
    ) -> str:
        return timezone.now().isoformat()