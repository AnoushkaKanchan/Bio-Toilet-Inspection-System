from rest_framework import serializers


class InspectionListItemSerializer(
    serializers.Serializer,
):
    inspection_id = serializers.CharField()
    train_number = serializers.CharField()
    pit_line = serializers.CharField()
    status = serializers.CharField()
    inspection_time = serializers.DateTimeField()
    duration_minutes = serializers.IntegerField()
    total_coaches = serializers.IntegerField()
    total_defects = serializers.IntegerField()
