from rest_framework import serializers


class InspectionListItemSerializer(serializers.Serializer,):
    inspection_id = serializers.CharField()
    train_number = serializers.CharField()
    train_name = serializers.CharField(allow_null=True,)
    inspection_time = serializers.DateTimeField()
    pit_line = serializers.CharField()
    status = serializers.CharField()
    issue_count = serializers.IntegerField()

class TrainInfoSerializer(serializers.Serializer,):
    number = serializers.CharField()
    name = serializers.CharField(allow_null=True,)

class InspectionSummarySerializer(serializers.Serializer,):
    started_at = serializers.DateTimeField()
    duration_minutes = serializers.IntegerField()
    coaches_detected = serializers.IntegerField()
    total_coaches = serializers.IntegerField()
    total_defects = serializers.IntegerField()

class DefectSummarySerializer(serializers.Serializer,):
    pipe_not_connected = serializers.IntegerField()
    pipe_support_absent = serializers.IntegerField()
    surface_not_clean = serializers.IntegerField()

class MappingStatusSerializer(serializers.Serializer,):
    completed = serializers.BooleanField()
    message = serializers.CharField()

class InspectionDetailsItemSerializer(serializers.Serializer,):
    inspection_id = serializers.CharField()
    status = serializers.CharField()
    pit_line = serializers.CharField()
    train = TrainInfoSerializer()
    inspection = InspectionSummarySerializer()
    defect_summary = DefectSummarySerializer()
    mapping = MappingStatusSerializer()

class CoachListItemSerializer(serializers.Serializer,):
    coach_id = serializers.CharField()
    inspection_sequence = serializers.IntegerField()
    coach_number = serializers.CharField()
    coach_type = serializers.CharField()
    status = serializers.CharField()
    left_side = serializers.CharField()
    right_side = serializers.CharField()
    confidence = serializers.FloatField()
    tank_count = serializers.IntegerField()
    defect_count = serializers.IntegerField()

class CoachListResponseSerializer(serializers.Serializer,):
    inspection_id = serializers.CharField()
    train_number = serializers.CharField()
    train_name = serializers.CharField(allow_null=True,)
    coaches = CoachListItemSerializer(many=True,)