class AIError(Exception):
    """
    Base exception for the AI bounded context.
    """


class AIContractError(AIError):
    """
    Raised when the AI payload violates the frozen API contract.
    """


class DuplicateAIResultError(AIError):
    """
    Raised when an AI result with the same inspection_run_id
    has already been persisted.

    AI inspection runs are immutable and cannot be overwritten.
    """


class AIResultNotFoundError(AIError):
    """
    Raised when the requested AI result cannot be found.
    """


class AIPersistenceError(AIError):
    """
    Raised when an unexpected persistence failure occurs while
    storing an AI result.
    """