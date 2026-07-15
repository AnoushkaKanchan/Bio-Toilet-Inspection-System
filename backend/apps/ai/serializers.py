from rest_framework import serializers


class TankSerializer(serializers.Serializer):
    coach_number = serializers.IntegerField()
    tank_id = serializers.CharField()
    camera_side = serializers.CharField()
    timestamp_sec = serializers.FloatField()
    maintenance_status = serializers.CharField()
    tank_image_path = serializers.CharField()
    surface_status = serializers.CharField()
    pipe_support_status = serializers.CharField()
    pipe_status = serializers.CharField()
    detection_confidence = serializers.FloatField()


class AIResultRequestSerializer(serializers.Serializer):
    inspection_run_id = serializers.CharField()

    processing_timestamp = serializers.DateTimeField()

    status = serializers.CharField()

    tanks = TankSerializer(
        many=True,
    )


class AIAcknowledgementSerializer(serializers.Serializer):
    success = serializers.BooleanField()

    inspection_id = serializers.UUIDField()

    message = serializers.CharField()