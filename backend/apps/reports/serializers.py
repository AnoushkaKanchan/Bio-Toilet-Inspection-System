from rest_framework import serializers


class TodaySummarySerializer(serializers.Serializer):
    trains_inspected = serializers.IntegerField()
    bio_tanks_inspected = serializers.IntegerField()
    defects_found = serializers.IntegerField()
    completed = serializers.IntegerField()


class WeeklySummarySerializer(serializers.Serializer):
    trains_inspected = serializers.IntegerField()
    coaches_inspected = serializers.IntegerField()
    bio_tanks_inspected = serializers.IntegerField()
    total_defects = serializers.IntegerField()


class MonthlySummarySerializer(serializers.Serializer):
    trains_inspected = serializers.IntegerField()
    coaches_inspected = serializers.IntegerField()
    bio_tanks_inspected = serializers.IntegerField()
    total_defects = serializers.IntegerField()


class DashboardSummarySerializer(serializers.Serializer):
    today = TodaySummarySerializer()
    weekly = WeeklySummarySerializer()
    monthly = MonthlySummarySerializer()


class CommonDefectSerializer(serializers.Serializer):
    defect_type = serializers.CharField()
    display_name = serializers.CharField()
    count = serializers.IntegerField()
