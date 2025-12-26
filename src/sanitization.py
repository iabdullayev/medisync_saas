"""Input sanitization utilities for security."""
import re
from typing import Optional


def sanitize_text_input(text: Optional[str], max_length: int = 500) -> str:
    """Sanitize user text input to prevent prompt injection and other attacks.
    
    Args:
        text: The text to sanitize
        max_length: Maximum allowed length for the text
        
    Returns:
        Sanitized text string
    """
    if not text:
        return ""
    
    # Remove control characters, keep only printable + newlines/tabs
    sanitized = ''.join(
        char for char in text 
        if char.isprintable() or char in '\n\r\t'
    )
    
    # Truncate to max length
    sanitized = sanitized[:max_length]
    
    # Remove potential prompt injection patterns
    injection_patterns = [
        r'ignore\s+previous\s+instructions',
        r'ignore\s+all\s+previous',
        r'system:',
        r'assistant:',
        r'###\s*instruction',
        r'<\|im_start\|>',
        r'<\|im_end\|>',
    ]
    
    for pattern in injection_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
    
    return sanitized.strip()


def sanitize_name(name: Optional[str]) -> str:
    """Sanitize name input (shorter length, stricter validation).
    
    Args:
        name: The name to sanitize
        
    Returns:
        Sanitized name string
    """
    return sanitize_text_input(name, max_length=100)


def sanitize_address(address: Optional[str]) -> str:
    """Sanitize address input (allows longer text).
    
    Args:
        address: The address to sanitize
        
    Returns:
        Sanitized address string
    """
    return sanitize_text_input(address, max_length=500)
