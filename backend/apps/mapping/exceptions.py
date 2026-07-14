class MappingError(Exception):
    """Base exception for mapping domain."""


class MappingValidationError(MappingError):
    """Raised when mapping input is invalid."""
