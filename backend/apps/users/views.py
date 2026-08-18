from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.exceptions import (
    AuthMethodNotEnabledError,
    InactiveUserError,
    InvalidCredentialsError,
    OTPAlreadyConsumedError,
    OTPExpiredError,
    OTPMaxAttemptsExceededError,
    UserNotFoundError,
)
from apps.users.repositories import HierarchyRepository
from apps.users.serializers import (
    HierarchyNodeSerializer,
    OTPRequestSerializer,
    OTPVerifySerializer,
    PasswordLoginSerializer,
    PitSerializer,
    TokenPairSerializer,
    UserProfileSerializer,
)
from apps.users.services.auth import AuthService
from apps.users.services.hierarchy import HierarchyService


class OTPRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = AuthService()

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self._service.request_otp(identifier=serializer.validated_data["identifier"])
        except (UserNotFoundError, InactiveUserError, AuthMethodNotEnabledError) as exc:
            return Response(
                {"success": False, "message": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"success": True, "message": "OTP sent."}, status=status.HTTP_200_OK)


class OTPVerifyAPIView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = AuthService()

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            tokens = self._service.verify_otp_and_login(
                identifier=serializer.validated_data["identifier"],
                code=serializer.validated_data["code"],
            )
        except (
            OTPExpiredError,
            OTPAlreadyConsumedError,
            OTPMaxAttemptsExceededError,
            AuthMethodNotEnabledError,
        ) as exc:
            return Response(
                {"success": False, "message": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except UserNotFoundError as exc:
            return Response(
                {"success": False, "message": str(exc)},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(TokenPairSerializer(tokens).data, status=status.HTTP_200_OK)


class PasswordLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = AuthService()

    def post(self, request):
        serializer = PasswordLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            tokens = self._service.login_with_password(
                identifier=serializer.validated_data["identifier"],
                password=serializer.validated_data["password"],
            )
        except (InvalidCredentialsError, InactiveUserError, AuthMethodNotEnabledError) as exc:
            return Response(
                {"success": False, "message": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(TokenPairSerializer(tokens).data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"success": False, "message": "'refresh' token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {"success": False, "message": "Invalid or already-revoked token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"success": True}, status=status.HTTP_205_RESET_CONTENT)


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserProfileSerializer(request.user).data, status=status.HTTP_200_OK)


class HierarchyTreeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._hierarchy_service = HierarchyService()
        self._repository = HierarchyRepository()

    def get(self, request):
        accessible_ids = self._hierarchy_service.get_accessible_node_ids(user=request.user)

        roots = self._repository.get_root_nodes()
        if accessible_ids is not None:
            roots = [node for node in roots if node.id in accessible_ids]

        # NOTE: for a large national hierarchy, replace this recursive
        # serialization with a single prefetch-based tree build.
        return Response(
            HierarchyNodeSerializer(roots, many=True).data,
            status=status.HTTP_200_OK,
        )


class DepotPitsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._hierarchy_service = HierarchyService()
        self._repository = HierarchyRepository()

    def get(self, request, depot_id):
        if not self._hierarchy_service.can_access_node(user=request.user, node_id=depot_id):
            return Response(
                {"success": False, "message": "Depot not in your accessible scope."},
                status=status.HTTP_403_FORBIDDEN,
            )

        pits = self._repository.get_pits_for_depot(depot_id=depot_id)
        return Response(PitSerializer(pits, many=True).data, status=status.HTTP_200_OK)