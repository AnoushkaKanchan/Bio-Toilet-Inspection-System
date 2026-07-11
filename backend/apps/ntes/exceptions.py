class NTESError(Exception):
    """
    Base exception for the NTES bounded context.
    """


class NTESClientError(NTESError):
    pass


class NTESParserError(NTESError):
    pass


class NTESValidationError(NTESError):
    pass


class NTESNormalizationError(NTESError):
    """Raised when parsed coach data cannot be normalized."""


class NTESPersistenceError(NTESError):
    pass


class NTESVerificationError(NTESError):
    """Raised when persisted NTES coach composition is invalid."""


class NTESSynchronizationError(NTESError):
    pass


class NTESUnavailableError(NTESError):
    """NTES website is unavailable."""


class TrainNotFoundError(NTESError):
    """Train number not found on NTES."""


class CoachCompositionNotFoundError(NTESError):
    """Coach Position could not be opened."""


class NTESParsingError(NTESError):
    """Raised by the HTML parser."""


class NTESClientTimeoutError(NTESError):
    """Playwright timeout while interacting with NTES."""
