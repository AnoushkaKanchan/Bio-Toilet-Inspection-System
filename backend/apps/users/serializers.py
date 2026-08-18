from rest_framework import serializers

from apps.users.models import HierarchyNode, Pit, User


class OTPRequestSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=225)


class OTPVerifySerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=225)
    code = serializers.CharField(max_length=10)


class PasswordLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=225)
    password = serializers.CharField(max_length=255, write_only=True)


class TokenPairSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class PitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pit
        fields = ["id", "name", "code", "active", "camera_configuration"]


class HierarchyNodeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = HierarchyNode
        fields = ["id", "type", "name", "code", "children"]

    def get_children(self, obj):
        children = getattr(obj, "_prefetched_children", None)
        if children is None:
            children = obj.children.all()
        return HierarchyNodeSerializer(children, many=True).data


class UserProfileSerializer(serializers.ModelSerializer):
    assigned_pits = PitSerializer(many=True, read_only=True)
    assigned_node = HierarchyNodeSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "mobile",
            "email",
            "role",
            "designation",
            "assigned_node",
            "assigned_pits",
            "is_active",
        ]