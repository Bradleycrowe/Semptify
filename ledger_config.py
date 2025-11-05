"""
Ledger Configuration Management

Provides centralized configuration for:
- Statute of limitations durations
- Time sensitivity settings
- Weather alert thresholds
- Notification preferences
- Retention policies

Configuration is stored in JSON and can be updated via admin panel.
"""

import os
import json
from typing import Dict, Any, Optional
from datetime import datetime


class LedgerConfig:
    """Manages ledger system configuration."""
    
    DEFAULT_CONFIG = {
        "statute_durations": {
            "eviction_notice": 60,
            "unlawful_detainer": 5,
            "answer_to_complaint": 30,
            "appeal_filing": 60,
            "discovery_motion": 45,
            "default_judgment": 10,
            "rent_demand": 3,
            "cure_or_quit": 30,
            "complaint": 365,
            "counterclaim": 30,
        },
        "time_sensitivities": {
            "service_deadline": {
                "duration_days": 60,
                "business_days_only": True,
                "exclude_holidays": True,
                "weather_dependent": True,
                "max_weather_extension_days": 7,
            },
            "answer_deadline": {
                "duration_days": 30,
                "business_days_only": True,
                "exclude_holidays": True,
                "weather_dependent": False,
            },
            "discovery_deadline": {
                "duration_days": 45,
                "business_days_only": True,
                "exclude_holidays": True,
                "weather_dependent": True,
                "max_weather_extension_days": 5,
            },
            "rent_payment": {
                "duration_days": 5,
                "business_days_only": False,
                "exclude_holidays": False,
                "weather_dependent": False,
            },
            "response_deadline": {
                "duration_days": 21,
                "business_days_only": True,
                "exclude_holidays": True,
                "weather_dependent": True,
                "max_weather_extension_days": 3,
            },
        },
        "weather_settings": {
            "severe_conditions": [
                "blizzard",
                "hurricane",
                "tornado",
                "flood",
                "ice_storm",
            ],
            "visibility_threshold_miles": 0.5,
            "wind_alert_threshold_mph": 40,
            "precipitation_threshold_inches": 2.0,
            "alert_types": [
                "flood_watch",
                "flood_warning",
                "tornado_watch",
                "tornado_warning",
                "hurricane_watch",
                "hurricane_warning",
                "winter_storm_warning",
                "blizzard_warning",
                "heat_advisory",
                "excessive_heat_warning",
            ],
        },
        "notification_settings": {
            "alert_days_before_statute_expiry": 30,
            "alert_days_before_service_deadline": 14,
            "alert_on_severe_weather": True,
            "alert_on_deadline_extension": True,
        },
        "retention_settings": {
            "keep_transactions_days": 2555,  # ~7 years (legal retention)
            "keep_weather_data_days": 365,
            "archive_expired_statutes": True,
        },
        "jurisdiction_settings": {
            "default_jurisdiction": "US",
            "state": "CA",
            "county": "",
        },
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to config JSON file. If None, uses default location.
        """
        if config_path is None:
            # Default to data/ledger_config.json
            config_path = os.path.join(os.getcwd(), "data", "ledger_config.json")
        
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from file, or use defaults if file doesn't exist."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
                # Merge with defaults to ensure all keys exist
                self.config = self._merge_with_defaults(self.config)
            except Exception as e:
                print(f"Warning: Could not load config from {self.config_path}: {e}")
                self.config = dict(self.DEFAULT_CONFIG)
        else:
            # Use defaults
            self.config = dict(self.DEFAULT_CONFIG)
            # Create config file with defaults
            self.save()
    
    def save(self) -> None:
        """Save configuration to file."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config to {self.config_path}: {e}")
    
    def _merge_with_defaults(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge loaded config with defaults to ensure all keys exist."""
        merged = dict(self.DEFAULT_CONFIG)
        
        for section, values in config.items():
            if section in merged:
                if isinstance(values, dict) and isinstance(merged[section], dict):
                    # Deep merge section
                    merged[section].update(values)
                else:
                    merged[section] = values
            else:
                merged[section] = values
        
        return merged
    
    def get(self, path: str, default: Any = None) -> Any:
        """Get config value by dot-notation path.
        
        Args:
            path: Dot-separated path like "statute_durations.eviction_notice"
            default: Default value if path doesn't exist
            
        Returns:
            Config value or default
        """
        parts = path.split(".")
        value = self.config
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        
        return value
    
    def set(self, path: str, value: Any) -> None:
        """Set config value by dot-notation path.
        
        Args:
            path: Dot-separated path like "statute_durations.eviction_notice"
            value: Value to set
        """
        parts = path.split(".")
        config = self.config
        
        # Navigate to parent
        for part in parts[:-1]:
            if part not in config:
                config[part] = {}
            config = config[part]
        
        # Set final value
        config[parts[-1]] = value
    
    def get_section(self, section: str) -> Optional[Dict[str, Any]]:
        """Get entire configuration section.
        
        Args:
            section: Top-level section name
            
        Returns:
            Section dict or None if not found
        """
        return self.config.get(section)
    
    def reset_to_defaults(self) -> None:
        """Reset all configuration to defaults."""
        self.config = dict(self.DEFAULT_CONFIG)
        self.save()
    
    def to_dict(self) -> Dict[str, Any]:
        """Get full configuration as dict."""
        return dict(self.config)


# =====================
# SINGLETON INSTANCE
# =====================

_ledger_config: Optional[LedgerConfig] = None


def get_ledger_config(config_path: Optional[str] = None) -> LedgerConfig:
    """Get the singleton ledger config instance.
    
    Args:
        config_path: Path to config file (only used on first call)
        
    Returns:
        LedgerConfig instance
    """
    global _ledger_config
    if _ledger_config is None:
        _ledger_config = LedgerConfig(config_path)
    return _ledger_config


def reset_config() -> None:
    """Reset config singleton (useful for testing)."""
    global _ledger_config
    _ledger_config = None
