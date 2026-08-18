class UserError(Exception):
    """Base exception for the users/RBAC bounded context."""


class InvalidCredentialsError(UserError):
    """Raised when login credentials (password or OTP) are incorrect."""


class OTPExpiredError(UserError):
    """Raised when an OTP has expired."""


class OTPAlreadyConsumedError(UserError):
    """Raised when an OTP has already been used."""


class OTPMaxAttemptsExceededError(UserError):
    """Raised when too many incorrect OTP attempts have been made."""


class AuthMethodNotEnabledError(UserError):
    """Raised when a requested login mode is not enabled for this deployment."""


class InactiveUserError(UserError):
    """Raised when a matched user account is inactive."""


class UserNotFoundError(UserError):
    """Raised when no user matches the given identifier."""