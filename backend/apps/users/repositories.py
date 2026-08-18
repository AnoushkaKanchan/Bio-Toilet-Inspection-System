from django.db.models import Q
from django.utils import timezone

from apps.users.models import OTP, HierarchyNode, Pit, User


class UserRepository:
    def get_by_id(self, *, user_id) -> User:
        return User.objects.select_related("assigned_node").get(id=user_id)

    def get_by_identifier(self, *, identifier: str) -> User | None:
        return (
            User.objects.select_related("assigned_node")
            .filter(Q(mobile=identifier) | Q(email__iexact=identifier))
            .first()
        )


class OTPRepository:
    def create(self, *, identifier: str, purpose: str, code_hash: str, expires_at) -> OTP:
        return OTP.objects.create(
            identifier=identifier,
            purpose=purpose,
            code_hash=code_hash,
            expires_at=expires_at,
        )

    def get_latest_active(self, *, identifier: str, purpose: str) -> OTP | None:
        return (
            OTP.objects.filter(
                identifier=identifier,
                purpose=purpose,
                consumed_at__isnull=True,
            )
            .order_by("-created_at")
            .first()
        )

    def increment_attempts(self, *, otp: OTP) -> OTP:
        otp.attempts += 1
        otp.save(update_fields=["attempts"])
        return otp

    def consume(self, *, otp: OTP) -> OTP:
        otp.consumed_at = timezone.now()
        otp.save(update_fields=["consumed_at"])
        return otp


class HierarchyRepository:
    def get_node(self, *, node_id) -> HierarchyNode:
        return HierarchyNode.objects.get(id=node_id)

    def get_children(self, *, node_id) -> list[HierarchyNode]:
        return list(HierarchyNode.objects.filter(parent_id=node_id))

    def get_root_nodes(self) -> list[HierarchyNode]:
        return list(HierarchyNode.objects.filter(parent__isnull=True))

    def get_pits_for_depot(self, *, depot_id) -> list[Pit]:
        return list(Pit.objects.filter(depot_id=depot_id, active=True))

    def get_pits_by_ids(self, *, pit_ids) -> list[Pit]:
        return list(Pit.objects.filter(id__in=pit_ids))