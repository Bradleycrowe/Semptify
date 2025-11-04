"""
Ledger Configuration Manager

Centralized configuration for ledger tracking, statute of limitations,
time sensitivities, and weather parameters. Supports:
- Environment variable overrides
- JSON config files
- Runtime updates via admin API
- Default sensible values
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import threading

_config_lock = threading.Lock()

CONFIG_DIR = Path("config")
CONFIG_DIR.mkdir(exist_ok=True)

DEFAULT_CONFIG = {
    "statute_durations": {
        "eviction_notice": 30,
        "cure_period": 5,
        "complaint": 365,
        "damage_claim": 1095,
        "lease_dispute": 730,
        "security_deposit": 90,
    },
    "time_sensitivities": {
        "eviction_notice_period": {
            "duration_days": 3,
            "weather_dependent": False,
            "holiday_dependent": True,
        },
        "cure_period": {
            "duration_days": 5,
            "weather_dependent": False,
            "holiday_dependent": True,
        },
        "service_deadline": {
            "duration_days": 90,
            "weather_dependent": True,
            "holiday_dependent": False,
        },
        "response_deadline": {
            "duration_days": 20,
            "weather_dependent": False,
            "holiday_dependent": True,
        },
    },
    "weather_settings": {
        "severe_conditions": ["snow", "extreme_heat", "extreme_cold", "flood"],
        "visibility_threshold_miles": 0.5,
        "wind_alert_threshold_mph": 40,
        "alert_types": [
            "flood_watch",
            "flood_warning",
            "snow_warning",
            "wind_advisory",
            "heat_advisory",
        ],
    },
    "ledger_settings": {
        "retention_days": 2555,  # ~7 years for statute compliance
        "archive_old_records": True,
        "enable_tamper_detection": True,
        "require_actor_verification": False,
    },
    "notification_settings": {
        "alert_days_before_statute_expiry": 30,
        "alert_days_before_service_deadline": 7,
        "alert_severe_weather_days_ahead": 3,
    },
}


class LedgerConfig:
    """Centralized configuration manager for ledger system."""

    def __init__(self):
        self.config_file = CONFIG_DIR / "ledger_config.json"
        self.config: Dict[str, Any] = {}
        self.load()

    def load(self):
        """Load configuration from file or use defaults."""
        with _config_lock:
            # Start with defaults
            self.config = json.loads(json.dumps(DEFAULT_CONFIG))

            # Override with file if it exists
            if self.config_file.exists():
                try:
                    file_config = json.loads(self.config_file.read_text())
                    self._deep_merge(self.config, file_config)
                    print(f"✓ Loaded config from {self.config_file}")
                except Exception as e:
                    print(f"⚠ Error loading config file: {e}, using defaults")

            # Override with environment variables
            self._load_from_env()

    def _load_from_env(self):
        """Load configuration overrides from environment variables.

        Format:
        SEMPTIFY_CONFIG_STATUTE_EVICTION_NOTICE=30
        SEMPTIFY_CONFIG_WEATHER_WIND_THRESHOLD=45
        """
        for key, value in os.environ.items():
            if key.startswith("SEMPTIFY_CONFIG_"):
                # Parse nested config path: SEMPTIFY_CONFIG_STATUTE_EVICTION_NOTICE
                parts = key[16:].lower().split("_")  # Remove prefix, lowercase, split

                try:
                    # Navigate to the right place in config
                    current = self.config
                    for part in parts[:-1]:
                        if part not in current:
                            current[part] = {}
                        current = current[part]

                    # Set the value (try to parse as number or boolean)
                    final_key = parts[-1]
                    if value.lower() in ("true", "false"):
                        current[final_key] = value.lower() == "true"
                    elif value.isdigit():
                        current[final_key] = int(value)
                    else:
                        try:
                            current[final_key] = float(value)
                        except ValueError:
                            current[final_key] = value

                    print(f"  Loaded from env: {key} = {value}")
                except Exception as e:
                    print(f"  ⚠ Error parsing {key}: {e}")

    def _deep_merge(self, target: Dict, source: Dict):
        """Recursively merge source into target."""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value

    def get(self, path: str, default: Any = None) -> Any:
        """Get config value by dot-notation path.

        Examples:
        - "statute_durations.eviction_notice"
        - "weather_settings.severity_threshold"
        - "notification_settings.alert_days_before_statute_expiry"
        """
        with _config_lock:
            parts = path.split(".")
            current = self.config

            for part in parts:
                if isinstance(current, dict):
                    current = current.get(part)
                    if current is None:
                        return default
                else:
                    return default

            return current if current is not None else default

    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire config section."""
        with _config_lock:
            return self.config.get(section, {})

    def set(self, path: str, value: Any):
        """Set config value by dot-notation path.

        Note: Changes are temporary (not persisted to file automatically).
        Call save() to persist.
        """
        with _config_lock:
            parts = path.split(".")
            current = self.config

            # Navigate to parent
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]

            # Set the value
            current[parts[-1]] = value

    def save(self):
        """Persist current configuration to file."""
        with _config_lock:
            try:
                self.config_file.write_text(json.dumps(self.config, indent=2))
                print(f"✓ Saved config to {self.config_file}")
                return True
            except Exception as e:
                print(f"✗ Error saving config: {e}")
                return False

    def reset_to_defaults(self):
        """Reset all config to defaults."""
        with _config_lock:
            self.config = json.loads(json.dumps(DEFAULT_CONFIG))
            self.save()

    def get_statute_duration(self, action_type: str) -> int:
        """Get statute duration in days for an action type."""
        durations = self.get_section("statute_durations")
        return durations.get(action_type, 365)  # Default 1 year

    def get_sensitivity(self, name: str) -> Optional[Dict[str, Any]]:
        """Get time sensitivity config."""
        sensitivities = self.get_section("time_sensitivities")
        return sensitivities.get(name)

    def is_severe_weather(self, condition: str) -> bool:
        """Check if weather condition is considered severe."""
        severe = self.get("weather_settings.severe_conditions", [])
        return condition in severe

    def get_alert_thresholds(self) -> Dict[str, int]:
        """Get all alert thresholds."""
        return self.get_section("notification_settings")

    def export_for_court_packet(self) -> Dict[str, Any]:
        """Export relevant config for court packet context."""
        return {
            "statute_of_limitations": self.get_section("statute_durations"),
            "service_requirements": self.get_section("time_sensitivities"),
            "generated_at": datetime.now().isoformat(),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Get full config as dictionary."""
        with _config_lock:
            return json.loads(json.dumps(self.config))


# Global instance
_config_instance: Optional[LedgerConfig] = None


def get_ledger_config() -> LedgerConfig:
    """Get or create global config instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = LedgerConfig()
    return _config_instance


def reload_config():
    """Reload configuration from disk and environment."""
    global _config_instance
    if _config_instance is not None:
        _config_instance.load()
