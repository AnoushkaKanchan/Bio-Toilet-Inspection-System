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
    pass


class NTESPersistenceError(NTESError):
    pass


class NTESVerificationError(NTESError):
    pass


class NTESSynchronizationError(NTESError):
    pass
