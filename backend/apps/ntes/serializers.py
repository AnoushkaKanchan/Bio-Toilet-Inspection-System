from rest_framework import serializers


class FetchTrainResponseSerializer(
    serializers.Serializer,
):
    success = serializers.BooleanField()
    inspection_id = serializers.UUIDField()
    coaches_synchronized = serializers.IntegerField()
    mapping_executed = serializers.BooleanField()

class FetchTrainRequestSerializer(serializers.Serializer):
    train_number = serializers.RegexField(
        regex=r"^\d{5}$",
        error_messages={
            "invalid": "Train number must be exactly 5 digits.",
        },
    )