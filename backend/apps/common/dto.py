from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceStatusDTO:
    name: str
    status: str

@dataclass(frozen=True)
class SystemStatusDTO:
    overall: str
    last_updated: str
    services: list[ServiceStatusDTO]

@dataclass(frozen=True)
class PreferencesDTO:
    auto_refresh: bool

@dataclass(frozen=True)
class SupportDTO:
    email: str

@dataclass(frozen=True)
class AboutDTO:
    application_name: str
    version: str
    technical_support: SupportDTO

@dataclass(frozen=True)
class SettingsDTO:
    system_status: SystemStatusDTO
    preferences: PreferencesDTO
    about: AboutDTO