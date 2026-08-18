from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings

from apps.users.exceptions import (
    AuthMethodNotEnabledError,
    InactiveUserError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from apps.users.models import AuthMethod, OTPPurpose, User
from apps.users.repositories import UserRepository
from apps.users.services.otp import OTPService


class AuthService:
    def __init__(
        self,
        *,
        user_repository: UserRepository | None = None,
        otp_service: OTPService | None = None,
    ) -> None:
        self._user_repository = user_repository or UserRepository()
        self._otp_service = otp_service or OTPService()

    def request_otp(self, *, identifier: str) -> None:
        self._ensure_method_enabled(AuthMethod.MOBILE_OTP, AuthMethod.EMAIL_OTP)

        user = self._user_repository.get_by_identifier(identifier=identifier)
        if user is None:
            raise UserNotFoundError("No account found for this identifier.")
        if not user.is_active:
            raise InactiveUserError("This account is inactive.")

        self._otp_service.request_otp(identifier=identifier, purpose=OTPPurpose.LOGIN)

    def verify_otp_and_login(self, *, identifier: str, code: str) -> dict:
        self._ensure_method_enabled(AuthMethod.MOBILE_OTP, AuthMethod.EMAIL_OTP)

        self._otp_service.verify_otp(
            identifier=identifier,
            purpose=OTPPurpose.LOGIN,
            code=code,
        )

        user = self._user_repository.get_by_identifier(identifier=identifier)
        if user is None:
            raise UserNotFoundError("No account found for this identifier.")

        return self._issue_tokens(user=user)

    def login_with_password(self, *, identifier: str, password: str) -> dict:
        self._ensure_method_enabled(AuthMethod.MOBILE_PASSWORD, AuthMethod.EMAIL_PASSWORD)

        user = self._user_repository.get_by_identifier(identifier=identifier)
        if user is None or not user.check_password(password):
            raise InvalidCredentialsError("Incorrect credentials.")
        if not user.is_active:
            raise InactiveUserError("This account is inactive.")

        return self._issue_tokens(user=user)

    def _issue_tokens(self, *, user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    def _ensure_method_enabled(self, *methods: str) -> None:
        enabled = set(settings.ENABLED_AUTH_METHODS)
        if not enabled.intersection(methods):
            raise AuthMethodNotEnabledError(
                "None of the requested login methods are enabled for this deployment."
            )