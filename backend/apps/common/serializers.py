from rest_framework import serializers


class ServiceStatusSerializer(
    serializers.Serializer,
):
    name = serializers.CharField()

    status = serializers.CharField()


class SystemStatusSerializer(
    serializers.Serializer,
):
    overall = serializers.CharField()

    last_updated = serializers.CharField()

    services = ServiceStatusSerializer(
        many=True,
    )


class PreferencesSerializer(
    serializers.Serializer,
):
    auto_refresh = serializers.BooleanField()


class TechnicalSupportSerializer(
    serializers.Serializer,
):
    email = serializers.EmailField()


class AboutSerializer(
    serializers.Serializer,
):
    application_name = serializers.CharField()

    version = serializers.CharField()

    technical_support = TechnicalSupportSerializer()


class SettingsSerializer(
    serializers.Serializer,
):
    system_status = SystemStatusSerializer()

    preferences = PreferencesSerializer()

    about = AboutSerializer()