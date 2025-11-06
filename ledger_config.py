"""
Ledger Configuration Management Module

Provides centralized configuration for ledger, weather, and time sensitivity settings.
"""

import os
import json
from typing import Dict, Any, Optional
from datetime import datetime


class LedgerConfig:
    """Manages ledger system configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize ledger configuration.
        
        Args:
            config_path: Path to configuration file. If None, uses default location.
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config: Dict[str, Any] = {}
        self.load()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path."""
        cwd = os.getcwd()
        config_dir = os.path.join(cwd, "data", "config")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "ledger_config.json")
    
    def _get_defaults(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            "statute_durations": {
                "eviction_notice": 30,
                "cure_period": 5,
                "complaint": 365,
                "debt_collection": 2190,  # 6 years in days
                "personal_injury": 730,  # 2 years
                "contract_breach": 1460,  # 4 years
                "property_damage": 1095,  # 3 years
            },
            "time_sensitivities": {
                "service_deadline": {
                    "duration_days": 20,
                    "weather_dependent": True,
                    "extension_days": 3,
                    "exclude_weekends": True,
                    "exclude_holidays": True,
                },
                "response_deadline": {
                    "duration_days": 30,
                    "weather_dependent": False,
                    "extension_days": 0,
                    "exclude_weekends": True,
                    "exclude_holidays": True,
                },
                "appeal_deadline": {
                    "duration_days": 60,
                    "weather_dependent": False,
                    "extension_days": 0,
                    "exclude_weekends": True,
                    "exclude_holidays": True,
                },
            },
            "weather_settings": {
                "severe_conditions": [
                    "thunderstorm",
                    "tornado",
                    "hurricane",
                    "blizzard",
                    "ice_storm",
                    "flood",
                ],
                "visibility_threshold_miles": 0.5,
                "wind_alert_threshold_mph": 40,
                "precipitation_threshold_inches": 2.0,
                "alert_types": [
                    "tornado_warning",
                    "severe_thunderstorm_warning",
                    "flash_flood_warning",
                    "blizzard_warning",
                    "ice_storm_warning",
                    "hurricane_warning",
                ],
            },
            "notification_settings": {
                "alert_days_before_statute_expiry": 30,
                "alert_days_before_service_deadline": 7,
                "alert_days_before_response_deadline": 7,
                "email_notifications_enabled": False,
                "sms_notifications_enabled": False,
            },
            "retention_policies": {
                "completed_transactions_days": 2555,  # 7 years
                "expired_statutes_days": 365,  # 1 year
                "weather_data_days": 365,  # 1 year
            },
        }
    
    def load(self):
        """Load configuration from file or use defaults."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self.config = self._merge_configs(self._get_defaults(), loaded_config)
            else:
                self.config = self._get_defaults()
                self.save()
        except Exception:
            # If loading fails, use defaults and continue
            self.config = self._get_defaults()
    
    def _merge_configs(self, default: Dict, override: Dict) -> Dict:
        """Recursively merge override config into default config."""
        result = default.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def save(self):
        """Save configuration to file."""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass
    
    def get(self, path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.
        
        Args:
            path: Dot-separated path (e.g., "statute_durations.eviction_notice")
            default: Default value if path not found
            
        Returns:
            Configuration value or default
        """
        parts = path.split('.')
        current = self.config
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        
        return current
    
    def set(self, path: str, value: Any):
        """Set a configuration value using dot notation.
        
        Args:
            path: Dot-separated path (e.g., "statute_durations.eviction_notice")
            value: Value to set
        """
        parts = path.split('.')
        current = self.config
        
        # Navigate to the parent of the target
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Set the final value
        current[parts[-1]] = value
    
    def get_section(self, section: str) -> Optional[Dict[str, Any]]:
        """Get an entire configuration section.
        
        Args:
            section: Section name (e.g., "statute_durations")
            
        Returns:
            Dictionary of section data or None if not found
        """
        return self.config.get(section)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self.config.copy()
    
    def reset_to_defaults(self):
        """Reset configuration to default values."""
        self.config = self._get_defaults()
        self.save()


# Singleton instance
_ledger_config: Optional[LedgerConfig] = None


def get_ledger_config() -> LedgerConfig:
    """Get the ledger configuration singleton."""
    global _ledger_config
    if _ledger_config is None:
        _ledger_config = LedgerConfig()
    return _ledger_config
