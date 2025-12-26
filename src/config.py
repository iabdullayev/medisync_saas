"""Centralized configuration management for MediSync SaaS."""
import streamlit as st
from typing import Optional
from dataclasses import dataclass


@dataclass
class AppConfig:
    """Application configuration loaded from Streamlit secrets."""
    
    groq_api_key: str
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None
    stripe_api_key: Optional[str] = None
    stripe_payment_link: Optional[str] = None

    @classmethod
    def from_secrets(cls) -> 'AppConfig':
        """Load configuration from Streamlit secrets.
        
        Returns:
            AppConfig: Configuration object with all secrets loaded.
        """
        return cls(
            groq_api_key=st.secrets.get("GROQ_API_KEY", ""),
            supabase_url=st.secrets.get("SUPABASE_URL"),
            supabase_key=st.secrets.get("SUPABASE_KEY"),
            stripe_api_key=st.secrets.get("STRIPE_API_KEY"),
            stripe_payment_link=st.secrets.get(
                "STRIPE_PAYMENT_LINK",
                "https://buy.stripe.com/test_14AeVfdef2bk7YJ248bAs00"
            )
        )

    def is_auth_enabled(self) -> bool:
        """Check if authentication is fully configured.
        
        Returns:
            bool: True if all auth-related secrets are present.
        """
        return all([self.supabase_url, self.supabase_key, self.stripe_api_key])
