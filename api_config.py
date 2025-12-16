"""
API Configuration System
Manages API keys, rate limits, provider fallbacks, and graceful degradation
"""
import os
from typing import Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
from pathlib import Path

@dataclass
class APIProvider:
    """Configuration for a single API provider"""
    name: str
    enabled: bool = False
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    rate_limit_per_minute: Optional[int] = None
    rate_limit_per_day: Optional[int] = None
    free_tier: bool = True
    requires_key: bool = True
    fallback_to: Optional[str] = None
    last_call: Optional[datetime] = None
    call_count_minute: int = 0
    call_count_day: int = 0
    last_error: Optional[str] = None


class APIConfig:
    """Central API configuration manager"""
    
    def __init__(self):
        self.providers: Dict[str, APIProvider] = {}
        self._load_from_env()
        self._load_from_file()
    
    def _load_from_env(self):
        """Load API configuration from environment variables"""
        
        # Legal APIs
        self.providers["courtlistener"] = APIProvider(
            name="CourtListener",
            api_key=os.getenv("COURT_LISTENER_API_KEY"),
            base_url="https://www.courtlistener.com/api/rest/v3",
            rate_limit_per_minute=50,
            rate_limit_per_day=5000,
            free_tier=True,
            requires_key=True
        )
        
        self.providers["govinfo"] = APIProvider(
            name="GovInfo",
            api_key=os.getenv("GOVINFO_API_KEY"),
            base_url="https://api.govinfo.gov",
            rate_limit_per_minute=1000,
            free_tier=True,
            requires_key=True
        )
        
        # Landlord Lookup APIs
        self.providers["rentcast"] = APIProvider(
            name="RentCast",
            api_key=os.getenv("RENTCAST_API_KEY"),
            base_url="https://api.rentcast.io/v1",
            rate_limit_per_minute=10,
            rate_limit_per_day=500,
            free_tier=True,
            requires_key=True
        )
        
        # Document Intelligence APIs
        self.providers["azure_document_intelligence"] = APIProvider(
            name="Azure Document Intelligence",
            api_key=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
            base_url=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
            rate_limit_per_minute=15,
            free_tier=True,
            requires_key=True
        )
        
        self.providers["google_vision"] = APIProvider(
            name="Google Vision API",
            api_key=os.getenv("GOOGLE_VISION_API_KEY"),
            base_url="https://vision.googleapis.com/v1",
            rate_limit_per_minute=60,
            rate_limit_per_day=1000,
            free_tier=True,
            requires_key=True,
            fallback_to="azure_document_intelligence"
        )
        
        # Multilingual APIs
        self.providers["libretranslate"] = APIProvider(
            name="LibreTranslate",
            api_key=os.getenv("LIBRETRANSLATE_API_KEY"),
            base_url=os.getenv("LIBRETRANSLATE_URL", "https://libretranslate.com"),
            rate_limit_per_minute=20,
            free_tier=True,
            requires_key=False
        )
        
        self.providers["deepl"] = APIProvider(
            name="DeepL",
            api_key=os.getenv("DEEPL_API_KEY"),
            base_url="https://api-free.deepl.com/v2" if os.getenv("DEEPL_FREE_TIER", "true").lower() == "true" else "https://api.deepl.com/v2",
            rate_limit_per_minute=None,  # Based on plan
            free_tier=True,
            requires_key=True,
            fallback_to="libretranslate"
        )
        
        self.providers["azure_translator"] = APIProvider(
            name="Microsoft Translator",
            api_key=os.getenv("AZURE_TRANSLATOR_KEY"),
            base_url="https://api.cognitive.microsofttranslator.com",
            rate_limit_per_minute=120,
            free_tier=True,
            requires_key=True,
            fallback_to="libretranslate"
        )
        
        self.providers["whisper"] = APIProvider(
            name="OpenAI Whisper",
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1",
            rate_limit_per_minute=50,
            free_tier=False,
            requires_key=True
        )
        
        # Finance APIs (mostly free, no keys)
        self.providers["yahoo_finance"] = APIProvider(
            name="Yahoo Finance",
            enabled=True,
            requires_key=False,
            free_tier=True
        )
        
        self.providers["coingecko"] = APIProvider(
            name="CoinGecko",
            api_key=os.getenv("COINGECKO_API_KEY"),  # Optional pro key
            base_url="https://api.coingecko.com/api/v3",
            rate_limit_per_minute=50,
            free_tier=True,
            requires_key=False
        )
        
        self.providers["exchangerate"] = APIProvider(
            name="ExchangeRate.host",
            enabled=True,
            base_url="https://api.exchangerate.host",
            requires_key=False,
            free_tier=True
        )
        
        # Housing APIs
        self.providers["openstreetmap"] = APIProvider(
            name="OpenStreetMap Nominatim",
            enabled=True,
            base_url="https://nominatim.openstreetmap.org",
            rate_limit_per_minute=1,  # Very conservative, respect their usage policy
            requires_key=False,
            free_tier=True
        )
        
        # Utility APIs
        self.providers["openweathermap"] = APIProvider(
            name="OpenWeatherMap",
            api_key=os.getenv("OPENWEATHER_API_KEY"),
            base_url="https://api.openweathermap.org/data/2.5",
            rate_limit_per_minute=60,
            rate_limit_per_day=1000,
            free_tier=True,
            requires_key=True
        )
        
        self.providers["restcountries"] = APIProvider(
            name="REST Countries",
            enabled=True,
            base_url="https://restcountries.com/v3.1",
            requires_key=False,
            free_tier=True
        )
        
        # Fun APIs
        self.providers["cat_api"] = APIProvider(
            name="The Cat API",
            api_key=os.getenv("CAT_API_KEY"),  # Optional
            base_url="https://api.thecatapi.com/v1",
            requires_key=False,
            free_tier=True
        )
        
        self.providers["dog_api"] = APIProvider(
            name="Dog CEO API",
            enabled=True,
            base_url="https://dog.ceo/api",
            requires_key=False,
            free_tier=True
        )
        
        self.providers["joke_api"] = APIProvider(
            name="JokeAPI",
            enabled=True,
            base_url="https://v2.jokeapi.dev",
            requires_key=False,
            free_tier=True
        )
        
        self.providers["nasa"] = APIProvider(
            name="NASA Open APIs",
            api_key=os.getenv("NASA_API_KEY", "DEMO_KEY"),
            base_url="https://api.nasa.gov",
            rate_limit_per_minute=30,
            rate_limit_per_day=1000,
            free_tier=True,
            requires_key=True
        )
        
        # Mark providers as enabled if they have keys (or don't require them)
        for provider in self.providers.values():
            if not provider.requires_key:
                provider.enabled = True
            elif provider.api_key:
                provider.enabled = True
    
    def _load_from_file(self):
        """Load additional config from JSON file"""
        config_file = Path("config/api_config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    # Override settings from file
                    for provider_name, settings in config_data.items():
                        if provider_name in self.providers:
                            for key, value in settings.items():
                                if hasattr(self.providers[provider_name], key):
                                    setattr(self.providers[provider_name], key, value)
            except Exception as e:
                print(f"Warning: Could not load config/api_config.json: {e}")
    
    def get_provider(self, name: str) -> Optional[APIProvider]:
        """Get provider configuration"""
        return self.providers.get(name)
    
    def is_enabled(self, name: str) -> bool:
        """Check if provider is enabled"""
        provider = self.providers.get(name)
        return provider.enabled if provider else False
    
    def get_api_key(self, name: str) -> Optional[str]:
        """Get API key for provider"""
        provider = self.providers.get(name)
        return provider.api_key if provider else None
    
    def get_base_url(self, name: str) -> Optional[str]:
        """Get base URL for provider"""
        provider = self.providers.get(name)
        return provider.base_url if provider else None
    
    def check_rate_limit(self, name: str) -> bool:
        """Check if rate limit allows another call"""
        provider = self.providers.get(name)
        if not provider:
            return False
        
        now = datetime.now()
        
        # Reset minute counter if needed
        if provider.last_call and (now - provider.last_call) > timedelta(minutes=1):
            provider.call_count_minute = 0
        
        # Reset day counter if needed
        if provider.last_call and (now - provider.last_call) > timedelta(days=1):
            provider.call_count_day = 0
        
        # Check limits
        if provider.rate_limit_per_minute and provider.call_count_minute >= provider.rate_limit_per_minute:
            return False
        
        if provider.rate_limit_per_day and provider.call_count_day >= provider.rate_limit_per_day:
            return False
        
        return True
    
    def record_call(self, name: str, success: bool = True, error: Optional[str] = None):
        """Record an API call"""
        provider = self.providers.get(name)
        if provider:
            provider.last_call = datetime.now()
            provider.call_count_minute += 1
            provider.call_count_day += 1
            if not success:
                provider.last_error = error
    
    def get_fallback(self, name: str) -> Optional[str]:
        """Get fallback provider if primary fails"""
        provider = self.providers.get(name)
        if provider and provider.fallback_to:
            fallback = self.providers.get(provider.fallback_to)
            if fallback and fallback.enabled:
                return provider.fallback_to
        return None
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get summary of all API statuses"""
        summary = {
            "total_providers": len(self.providers),
            "enabled_providers": sum(1 for p in self.providers.values() if p.enabled),
            "disabled_providers": sum(1 for p in self.providers.values() if not p.enabled),
            "providers": {}
        }
        
        for name, provider in self.providers.items():
            summary["providers"][name] = {
                "enabled": provider.enabled,
                "has_key": bool(provider.api_key),
                "requires_key": provider.requires_key,
                "free_tier": provider.free_tier,
                "rate_limit_minute": provider.rate_limit_per_minute,
                "calls_this_minute": provider.call_count_minute,
                "calls_today": provider.call_count_day,
                "last_call": provider.last_call.isoformat() if provider.last_call else None,
                "last_error": provider.last_error
            }
        
        return summary


# Singleton instance
_api_config = None

def get_api_config() -> APIConfig:
    """Get or create API configuration singleton"""
    global _api_config
    if _api_config is None:
        _api_config = APIConfig()
    return _api_config
