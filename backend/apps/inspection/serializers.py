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

class CoachInfoSerializer(serializers.Serializer,):
    number = serializers.CharField()
    type = serializers.CharField()
    status = serializers.CharField()

class CoachInspectionSummarySerializer(serializers.Serializer,):
    left_status = serializers.CharField()
    right_status = serializers.CharField()
    overall_confidence = serializers.IntegerField()

class HealthDiagramSerializer(serializers.Serializer,):
    front_left = serializers.CharField()
    front_right = serializers.CharField()
    rear_left = serializers.CharField()
    rear_right = serializers.CharField()
    bio_tank = serializers.CharField()

class FindingSerializer(serializers.Serializer,):
    title = serializers.CharField()
    description = serializers.CharField()
    confidence = serializers.IntegerField()

class NavigationSerializer(serializers.Serializer,):
    previous = serializers.CharField(allow_null=True,)
    next = serializers.CharField(allow_null=True,)

class CoachInspectionReportSerializer(serializers.Serializer,):
    coach = CoachInfoSerializer()
    inspection = CoachInspectionSummarySerializer()
    health_diagram = HealthDiagramSerializer()
    findings = FindingSerializer(many=True,)
    maintenance = serializers.ListField(child=serializers.CharField(),)
    remarks = serializers.CharField()
    navigation = NavigationSerializer()