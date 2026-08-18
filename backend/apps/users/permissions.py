from rest_framework.permissions import BasePermission

from apps.users.models import ROLE_RANK, Role
from apps.users.services.hierarchy import HierarchyService


def has_minimum_role(*, user, minimum: Role) -> bool:
    return ROLE_RANK[user.role] >= ROLE_RANK[minimum]


class MinimumRole(BasePermission):
    """
    Usage: permission_classes = [MinimumRole.of(Role.ADMIN)]
    """

    minimum_role: str = Role.SUPERVISOR

    @classmethod
    def of(cls, minimum_role: str):
        return type(
            f"MinimumRole{minimum_role.title().replace('_', '')}",
            (cls,),
            {"minimum_role": minimum_role},
        )

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and has_minimum_role(user=request.user, minimum=self.minimum_role)
        )


class HierarchyScopePermission(BasePermission):
    """
    Object-level permission: confirms the requested object's hierarchy node
    (or pit) is within the requesting user's accessible scope.

    The view is responsible for calling has_object_permission with an
    object exposing either `.hierarchy_node_id` or `.pit_id`.
    """

    def __init__(self, hierarchy_service: HierarchyService | None = None) -> None:
        self._hierarchy_service = hierarchy_service or HierarchyService()

    def has_object_permission(self, request, view, obj) -> bool:
        pit_id = getattr(obj, "pit_id", None)
        if pit_id is not None:
            return self._hierarchy_service.can_access_pit(user=request.user, pit_id=pit_id)

        node_id = getattr(obj, "hierarchy_node_id", None)
        if node_id is not None:
            return self._hierarchy_service.can_access_node(user=request.user, node_id=node_id)

        # No scope attribute found on the object — fail closed.
        return False