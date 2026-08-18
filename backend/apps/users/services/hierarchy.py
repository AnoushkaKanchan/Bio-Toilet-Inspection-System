from apps.users.models import HierarchyNode, HierarchyNodeType, Pit, Role, User
from apps.users.repositories import HierarchyRepository


class HierarchyService:
    def __init__(self, repository: HierarchyRepository | None = None) -> None:
        self._repository = repository or HierarchyRepository()

    def get_accessible_node_ids(self, *, user: User) -> set | None:
        """
        Returns the set of HierarchyNode ids the user can see (their assigned
        node plus every descendant). Returns None to mean "unrestricted"
        (Master Admin with assigned_node = None).
        """
        if user.role == Role.MASTER_ADMIN and user.assigned_node_id is None:
            return None

        if user.assigned_node_id is None:
            # Defensive: any non-Master-Admin user must have a scope node.
            return set()

        accessible = {user.assigned_node_id}
        frontier = [user.assigned_node_id]

        while frontier:
            next_frontier = []
            for node_id in frontier:
                for child in self._repository.get_children(node_id=node_id):
                    if child.id not in accessible:
                        accessible.add(child.id)
                        next_frontier.append(child.id)
            frontier = next_frontier

        return accessible

    def get_accessible_depot_ids(self, *, user: User) -> set | None:
        node_ids = self.get_accessible_node_ids(user=user)
        if node_ids is None:
            return None

        return {
            node.id
            for node in HierarchyNode.objects.filter(id__in=node_ids)
            if node.type == HierarchyNodeType.DEPOT
        }

    def get_accessible_pit_ids(self, *, user: User) -> set | None:
        """
        Combines hierarchy scope with the optional per-user Pit narrowing
        (Supervisors may be scoped to specific pits within their depot).
        """
        depot_ids = self.get_accessible_depot_ids(user=user)

        if depot_ids is None:
            pit_qs = Pit.objects.filter(active=True)
        else:
            pit_qs = Pit.objects.filter(depot_id__in=depot_ids, active=True)

        assigned_pit_ids = set(user.assigned_pits.values_list("id", flat=True))
        if assigned_pit_ids:
            pit_qs = pit_qs.filter(id__in=assigned_pit_ids)

        return set(pit_qs.values_list("id", flat=True))

    def can_access_node(self, *, user: User, node_id) -> bool:
        accessible = self.get_accessible_node_ids(user=user)
        return accessible is None or node_id in accessible

    def can_access_pit(self, *, user: User, pit_id) -> bool:
        accessible = self.get_accessible_pit_ids(user=user)
        return accessible is None or pit_id in accessible