"""Custom exception classes for MediSync application."""


class MediSyncError(Exception):
    """Base exception for all MediSync application errors."""
    pass


class OCRError(MediSyncError):
    """Raised when OCR processing fails."""
    pass


class LLMError(MediSyncError):
    """Raised when LLM generation fails."""
    pass


class AuthError(MediSyncError):
    """Raised when authentication fails."""
    pass


class ValidationError(MediSyncError):
    """Raised when input validation fails."""
    pass


class RateLimitError(MediSyncError):
    """Raised when rate limit is exceeded."""
    pass
