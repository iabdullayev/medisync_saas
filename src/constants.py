"""Application-wide constants and configuration values."""
from typing import Final

# ============================================================================
# OCR Configuration
# ============================================================================
OCR_DPI: Final[int] = 200
"""DPI for PDF to image conversion. 200 provides optimal balance of speed/quality."""

OCR_PSM_MODE: Final[str] = '--psm 6'
"""Tesseract Page Segmentation Mode. PSM 6 assumes uniform text block."""

# ============================================================================
# LLM Configuration
# ============================================================================
MAX_CONTEXT_LENGTH: Final[int] = 6000
"""Maximum context length for LLM prompts (token limit for Groq API)."""

LLM_MODEL: Final[str] = "llama-3.1-8b-instant"
"""Default LLM model for appeal generation."""

LLM_TEMPERATURE: Final[float] = 0.1
"""Temperature for LLM generation. Lower = more deterministic."""

# ============================================================================
# Security Configuration
# ============================================================================
MIN_PASSWORD_LENGTH: Final[int] = 8
"""Minimum password length for security compliance."""

MAX_EMAIL_LENGTH: Final[int] = 320
"""Maximum email length per RFC 5321."""

MAX_NAME_LENGTH: Final[int] = 100
"""Maximum length for name inputs."""

MAX_ADDRESS_LENGTH: Final[int] = 500
"""Maximum length for address inputs."""

# ============================================================================
# Rate Limiting Configuration
# ============================================================================
RATE_LIMIT_REQUESTS: Final[int] = 5
"""Maximum number of requests allowed per time window."""

RATE_LIMIT_WINDOW: Final[int] = 60
"""Rate limit time window in seconds."""

# ============================================================================
# Subscription Configuration
# ============================================================================
FREE_TRIAL_DAYS: Final[int] = 7
"""Number of days for free trial period."""

DEFAULT_STRIPE_PAYMENT_LINK: Final[str] = "https://buy.stripe.com/test_14AeVfdef2bk7YJ248bAs00"
"""Default Stripe payment link for subscriptions."""
