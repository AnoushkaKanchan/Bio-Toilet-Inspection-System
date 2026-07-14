from rest_framework import serializers


class AIResultRequestSerializer(
    serializers.Serializer,
):
    inspection_id = serializers.UUIDField()

    payload = serializers.JSONField()


class AIAcknowledgementSerializer(
    serializers.Serializer,
):
    success = serializers.BooleanField()

    inspection_id = serializers.CharField()

    message = serializers.CharField()