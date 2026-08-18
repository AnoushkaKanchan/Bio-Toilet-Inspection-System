import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Role(models.TextChoices):
    """
    Ordered from lowest to highest privilege.
    PRD §3 — Users, Roles and Railway Hierarchy.
    """

    SUPERVISOR = "SUPERVISOR", "Supervisor"
    OFFICER = "OFFICER", "Officer"
    ADMIN = "ADMIN", "Admin"
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    MASTER_ADMIN = "MASTER_ADMIN", "Master Admin"


# Numeric rank used by permission checks (higher = more privilege).
# Keep this in sync with Role.choices order.
ROLE_RANK = {
    Role.SUPERVISOR: 1,
    Role.OFFICER: 2,
    Role.ADMIN: 3,
    Role.SUPER_ADMIN: 4,
    Role.MASTER_ADMIN: 5,
}


class AuthMethod(models.TextChoices):
    MOBILE_OTP = "MOBILE_OTP", "Mobile + OTP"
    MOBILE_PASSWORD = "MOBILE_PASSWORD", "Mobile + Password"
    EMAIL_OTP = "EMAIL_OTP", "Email + OTP"
    EMAIL_PASSWORD = "EMAIL_PASSWORD", "Email + Password"


class HierarchyNodeType(models.TextChoices):
    """
    PRD §3.1 — Indian Railways -> Zone -> Division -> Coaching Depot -> Pit ...
    Indian Railways itself is not modeled as a row; Master Admin scope
    (assigned_node = None) implicitly means "all zones".
    """

    ZONE = "ZONE", "Zone"
    DIVISION = "DIVISION", "Division"
    DEPOT = "DEPOT", "Coaching Depot"


class HierarchyNode(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    type = models.CharField(
        max_length=20,
        choices=HierarchyNodeType.choices,
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
        help_text="Null only for top-level Zone nodes.",
    )

    name = models.CharField(max_length=150)

    code = models.CharField(
        max_length=30,
        help_text="Short railway code, e.g. 'WR', 'BCT'.",
    )

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hierarchy_node"
        ordering = ["type", "name"]
        verbose_name = "Hierarchy Node"
        verbose_name_plural = "Hierarchy Nodes"
        constraints = [
            models.UniqueConstraint(
                fields=["type", "code"],
                name="unique_code_per_type",
            ),
        ]

    def clean(self):
        # Enforce the fixed tree shape: ZONE has no parent,
        # DIVISION's parent must be a ZONE, DEPOT's parent must be a DIVISION.
        expected_parent_type = {
            HierarchyNodeType.ZONE: None,
            HierarchyNodeType.DIVISION: HierarchyNodeType.ZONE,
            HierarchyNodeType.DEPOT: HierarchyNodeType.DIVISION,
        }[self.type]

        if expected_parent_type is None and self.parent is not None:
            raise ValidationError("A Zone node cannot have a parent.")

        if expected_parent_type is not None:
            if self.parent is None:
                raise ValidationError(
                    f"A {self.type} node must have a parent of type {expected_parent_type}."
                )
            if self.parent.type != expected_parent_type:
                raise ValidationError(
                    f"A {self.type} node's parent must be of type {expected_parent_type}, "
                    f"got {self.parent.type}."
                )

    def __str__(self):
        return f"{self.type}: {self.name} ({self.code})"


class Pit(models.Model):
    """
    PRD §5 — Pit entity. Current site has five; must remain configurable
    (no code should assume an exact count).
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    depot = models.ForeignKey(
        HierarchyNode,
        on_delete=models.PROTECT,
        related_name="pits",
        limit_choices_to={"type": HierarchyNodeType.DEPOT},
    )

    name = models.CharField(max_length=100)

    code = models.CharField(max_length=30)

    active = models.BooleanField(default=True)

    camera_configuration = models.JSONField(
        default=dict,
        blank=True,
        help_text="Camera/side labels, calibration refs, etc. (deployment-configurable).",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pit"
        ordering = ["depot", "name"]
        verbose_name = "Pit"
        verbose_name_plural = "Pits"
        constraints = [
            models.UniqueConstraint(
                fields=["depot", "code"],
                name="unique_pit_code_per_depot",
            ),
        ]

    def clean(self):
        if self.depot_id and self.depot.type != HierarchyNodeType.DEPOT:
            raise ValidationError("Pit.depot must reference a DEPOT node.")

    def __str__(self):
        return f"{self.name} ({self.depot.code})"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, *, mobile=None, email=None, password=None, **extra_fields):
        if not mobile and not email:
            raise ValueError("User requires a mobile number or an email address.")

        if email:
            email = self.normalize_email(email)

        user = self.model(mobile=mobile, email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_user(self, *, mobile=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            mobile=mobile,
            email=email,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, *, mobile=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Role.MASTER_ADMIN)
        return self._create_user(
            mobile=mobile,
            email=email,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    """
    PRD §3 / §3.2. Hierarchy scope is a single HierarchyNode (the node the
    user is assigned at); access to descendants is resolved in
    services/hierarchy.py, not stored redundantly here.

    assigned_node = None means Master Admin (global) scope.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(max_length=150)

    mobile = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
    )

    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SUPERVISOR,
    )

    designation = models.CharField(max_length=150, blank=True)

    assigned_node = models.ForeignKey(
        HierarchyNode,
        on_delete=models.PROTECT,
        related_name="assigned_users",
        null=True,
        blank=True,
        help_text="Null implies Master Admin / global scope.",
    )

    # Supervisors may optionally be narrowed to specific pits within their
    # depot rather than the whole depot (PRD: 'Assigned depot and pits').
    assigned_pits = models.ManyToManyField(
        Pit,
        related_name="assigned_users",
        blank=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"
        ordering = ["name"]
        verbose_name = "User"
        verbose_name_plural = "Users"
        constraints = [
            models.CheckConstraint(
                check=models.Q(mobile__isnull=False) | models.Q(email__isnull=False),
                name="user_requires_mobile_or_email",
            ),
        ]

    def clean(self):
        if self.role != Role.MASTER_ADMIN and self.assigned_node_id is None:
            raise ValidationError(
                "Only Master Admin users may have an unset (global) hierarchy scope."
            )

    def has_minimum_role(self, minimum: Role) -> bool:
        return ROLE_RANK[self.role] >= ROLE_RANK[minimum]

    def __str__(self):
        return f"{self.name} ({self.role})"


class OTPPurpose(models.TextChoices):
    LOGIN = "LOGIN", "Login"
    PASSWORD_RESET = "PASSWORD_RESET", "Password Reset"


class OTP(models.Model):
    """
    Short-lived OTP challenge. Code is stored hashed; never stored/logged
    in plaintext outside of the delivery channel at send-time.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    identifier = models.CharField(
        max_length=225,
        help_text="Mobile number or email the OTP was issued to.",
    )

    purpose = models.CharField(
        max_length=20,
        choices=OTPPurpose.choices,
        default=OTPPurpose.LOGIN,
    )

    code_hash = models.CharField(max_length=255)

    attempts = models.PositiveSmallIntegerField(default=0)

    expires_at = models.DateTimeField()

    consumed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "otp"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["identifier", "purpose"]),
        ]
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    @property
    def is_consumed(self) -> bool:
        return self.consumed_at is not None

    def __str__(self):
        return f"OTP for {self.identifier} ({self.purpose})"