"""Rate limiting middleware for API protection."""
import time
from collections import defaultdict
from typing import Dict, List, Tuple


class RateLimiter:
    """Simple in-memory rate limiter using sliding window algorithm."""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        """Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed in the window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)
    
    def is_allowed(self, user_id: str) -> Tuple[bool, int]:
        """Check if a request from the user is allowed.
        
        Args:
            user_id: Unique identifier for the user (e.g., email)
            
        Returns:
            Tuple of (is_allowed, seconds_until_reset)
        """
        now = time.time()
        user_requests = self.requests[user_id]
        
        # Remove old requests outside the sliding window
        user_requests[:] = [
            req_time for req_time in user_requests 
            if now - req_time < self.window_seconds
        ]
        
        # Check if limit exceeded
        if len(user_requests) >= self.max_requests:
            oldest_request = min(user_requests)
            reset_time = int(self.window_seconds - (now - oldest_request))
            return False, reset_time
        
        # Allow request and record timestamp
        user_requests.append(now)
        return True, 0
    
    def get_remaining_requests(self, user_id: str) -> int:
        """Get the number of remaining requests for a user.
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Number of remaining requests in the current window
        """
        now = time.time()
        user_requests = self.requests[user_id]
        
        # Count valid requests in current window
        valid_requests = [
            req_time for req_time in user_requests 
            if now - req_time < self.window_seconds
        ]
        
        return max(0, self.max_requests - len(valid_requests))
