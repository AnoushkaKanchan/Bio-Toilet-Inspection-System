from rest_framework import serializers


class FetchTrainResponseSerializer(
    serializers.Serializer,
):
    success = serializers.BooleanField()
    inspection_id = serializers.UUIDField()
    coaches_synchronized = serializers.IntegerField()
    mapping_executed = serializers.BooleanField()