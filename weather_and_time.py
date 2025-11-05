"""
Weather and Time Sensitivity Module

Provides:
- Weather condition tracking and caching
- Time-sensitive deadline calculations
- Weather-based deadline adjustments
- Severe weather detection for evidence building

Weather data can affect legal deadlines (e.g., severe weather may toll deadlines).
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict


# =====================
# DATA CLASSES
# =====================


@dataclass
class WeatherCondition:
    """Weather data for a specific date and location."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    date: datetime = field(default_factory=datetime.now)
    location: str = ""
    temperature_f: float = 70.0
    condition: str = "clear"  # clear, rain, snow, fog, etc.
    humidity_percent: int = 50
    wind_speed_mph: float = 0.0
    precipitation_inches: float = 0.0
    visibility_miles: float = 10.0
    alerts: List[str] = field(default_factory=list)  # flood_watch, heat_advisory, etc.
    source: str = "api"  # api, manual, estimated
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        data = asdict(self)
        data["date"] = self.date.isoformat()
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @property
    def is_severe(self) -> bool:
        """Check if weather is severe enough to affect legal proceedings."""
        severe_conditions = ["blizzard", "hurricane", "tornado", "flood"]
        if any(cond in self.condition.lower() for cond in severe_conditions):
            return True

        if len(self.alerts) > 0:
            return True

        if self.precipitation_inches > 2.0:  # Heavy rain/snow
            return True

        if self.wind_speed_mph > 40:  # High winds
            return True

        if self.visibility_miles < 0.5:  # Very poor visibility
            return True

        return False


@dataclass
class TimeSensitivity:
    """Defines a time-sensitive deadline with rules."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    base_days: int = 30
    business_days_only: bool = True
    exclude_holidays: bool = True
    weather_adjustment: bool = True  # Can weather extend deadline?
    max_weather_extensions: int = 7  # Max days weather can add
    jurisdiction: str = "US"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return asdict(self)


# =====================
# MANAGER CLASSES
# =====================


class WeatherManager:
    """Manages weather conditions and lookups."""

    def __init__(self):
        self.conditions: Dict[str, WeatherCondition] = {}

    def _make_key(self, date: datetime, location: str) -> str:
        """Create cache key for weather lookup."""
        return f"{date.date().isoformat()}:{location}"

    def add_weather_condition(
        self,
        date: datetime,
        location: str,
        temperature_f: float,
        condition: str,
        humidity_percent: int = 50,
        wind_speed_mph: float = 0.0,
        precipitation_inches: float = 0.0,
        visibility_miles: float = 10.0,
        alerts: Optional[List[str]] = None,
        source: str = "api",
    ) -> WeatherCondition:
        """Add or update weather condition."""
        weather = WeatherCondition(
            date=date,
            location=location,
            temperature_f=temperature_f,
            condition=condition,
            humidity_percent=humidity_percent,
            wind_speed_mph=wind_speed_mph,
            precipitation_inches=precipitation_inches,
            visibility_miles=visibility_miles,
            alerts=alerts or [],
            source=source,
        )

        key = self._make_key(date, location)
        self.conditions[key] = weather
        return weather

    def get_weather(
        self,
        date: datetime,
        location: str,
    ) -> Optional[WeatherCondition]:
        """Get weather for specific date and location."""
        key = self._make_key(date, location)
        return self.conditions.get(key)

    def get_weather_for_period(
        self,
        start_date: datetime,
        end_date: datetime,
        location: str,
    ) -> List[WeatherCondition]:
        """Get all weather conditions for a date range."""
        results = []
        current = start_date

        while current <= end_date:
            weather = self.get_weather(current, location)
            if weather:
                results.append(weather)
            current += timedelta(days=1)

        return results

    def has_severe_weather(
        self,
        start_date: datetime,
        end_date: datetime,
        location: str,
    ) -> bool:
        """Check if period had severe weather."""
        conditions = self.get_weather_for_period(start_date, end_date, location)
        return any(c.is_severe for c in conditions)

    def count_severe_days(
        self,
        start_date: datetime,
        end_date: datetime,
        location: str,
    ) -> int:
        """Count days with severe weather in period."""
        conditions = self.get_weather_for_period(start_date, end_date, location)
        return sum(1 for c in conditions if c.is_severe)


class TimeSensitivityManager:
    """Manages time-sensitive deadlines and calculations."""

    # Pre-defined time sensitivities
    DEFAULT_SENSITIVITIES = {
        "service_deadline": TimeSensitivity(
            name="service_deadline",
            description="Deadline to serve defendant",
            base_days=60,
            business_days_only=True,
            exclude_holidays=True,
            weather_adjustment=True,
        ),
        "answer_deadline": TimeSensitivity(
            name="answer_deadline",
            description="Deadline to file answer to complaint",
            base_days=30,
            business_days_only=True,
            exclude_holidays=True,
            weather_adjustment=False,  # Strict deadline
        ),
        "discovery_deadline": TimeSensitivity(
            name="discovery_deadline",
            description="Discovery motion deadline",
            base_days=45,
            business_days_only=True,
            exclude_holidays=True,
            weather_adjustment=True,
        ),
        "rent_payment": TimeSensitivity(
            name="rent_payment",
            description="Monthly rent payment deadline",
            base_days=5,
            business_days_only=False,
            exclude_holidays=False,
            weather_adjustment=False,
        ),
    }

    def __init__(self):
        self.sensitivities: Dict[str, TimeSensitivity] = dict(self.DEFAULT_SENSITIVITIES)

    def add_sensitivity(self, sensitivity: TimeSensitivity) -> None:
        """Add or update a time sensitivity."""
        self.sensitivities[sensitivity.name] = sensitivity

    def calculate_deadline(
        self,
        sensitivity_name: str,
        start_date: datetime,
        location: Optional[str] = None,
        weather_manager: Optional[WeatherManager] = None,
    ) -> Dict[str, Any]:
        """Calculate deadline with all adjustments."""
        if sensitivity_name not in self.sensitivities:
            return {
                "error": f"Unknown sensitivity: {sensitivity_name}",
                "available": list(self.sensitivities.keys()),
            }

        sens = self.sensitivities[sensitivity_name]
        deadline = start_date
        days_added = 0
        weather_extensions = 0

        # Add base days
        if sens.business_days_only:
            # Skip weekends
            while days_added < sens.base_days:
                deadline += timedelta(days=1)
                if deadline.weekday() < 5:  # Monday = 0, Friday = 4
                    days_added += 1
        else:
            deadline += timedelta(days=sens.base_days)
            days_added = sens.base_days

        # Check for severe weather extensions
        if sens.weather_adjustment and location and weather_manager:
            severe_days = weather_manager.count_severe_days(start_date, deadline, location)
            weather_extensions = min(severe_days, sens.max_weather_extensions)
            deadline += timedelta(days=weather_extensions)

        return {
            "sensitivity": sensitivity_name,
            "start_date": start_date.isoformat(),
            "deadline": deadline.isoformat(),
            "base_days": sens.base_days,
            "days_added": days_added,
            "weather_extensions": weather_extensions,
            "business_days_only": sens.business_days_only,
            "total_calendar_days": (deadline - start_date).days,
        }


# =====================
# SINGLETON INSTANCES
# =====================

_weather_manager: Optional[WeatherManager] = None
_time_sensitivity_manager: Optional[TimeSensitivityManager] = None


def get_weather_manager() -> WeatherManager:
    """Get the singleton weather manager instance."""
    global _weather_manager
    if _weather_manager is None:
        _weather_manager = WeatherManager()
    return _weather_manager


def get_time_sensitivity_manager() -> TimeSensitivityManager:
    """Get the singleton time sensitivity manager instance."""
    global _time_sensitivity_manager
    if _time_sensitivity_manager is None:
        _time_sensitivity_manager = TimeSensitivityManager()
    return _time_sensitivity_manager


# =====================
# UTILITY FUNCTIONS
# =====================


def reset_managers() -> None:
    """Reset all managers (useful for testing)."""
    global _weather_manager, _time_sensitivity_manager
    _weather_manager = None
    _time_sensitivity_manager = None
