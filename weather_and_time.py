"""
Semptify Weather & Environmental Conditions Module

Integrates weather data with calendar events for:
- Service date validation (weather-dependent deadlines)
- Time-sensitive operations (weather windows)
- Court packet context (weather conditions at time of service)
- Sensitivity logic for time schedules
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path
import threading

# Thread-safe operations
_weather_lock = threading.Lock()

WEATHER_DIR = Path("weather_cache")
WEATHER_DIR.mkdir(exist_ok=True)


@dataclass
class WeatherCondition:
    """Weather snapshot for a specific date/time."""

    date: datetime
    location: str  # Address or coordinate
    temperature_f: float
    condition: str  # "clear", "rain", "snow", "fog", "extreme_heat", "extreme_cold"
    humidity_percent: int
    wind_speed_mph: float
    precipitation_inches: float
    visibility_miles: float
    alerts: List[str]  # "flood_watch", "snow_warning", etc.
    source: str  # "weather_api", "cached", "estimated"
    cached_at: datetime = None

    def __post_init__(self):
        if self.cached_at is None:
            self.cached_at = datetime.now()

    def is_severe(self) -> bool:
        """Check if weather is severe enough to affect service."""
        severe_conditions = ["snow", "extreme_heat", "extreme_cold", "flood"]
        return (
            self.condition in severe_conditions
            or len(self.alerts) > 0
            or self.visibility_miles < 0.5
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "date": self.date.isoformat(),
            "location": self.location,
            "temperature_f": self.temperature_f,
            "condition": self.condition,
            "humidity_percent": self.humidity_percent,
            "wind_speed_mph": self.wind_speed_mph,
            "precipitation_inches": self.precipitation_inches,
            "visibility_miles": self.visibility_miles,
            "alerts": self.alerts,
            "source": self.source,
            "cached_at": self.cached_at.isoformat(),
            "is_severe": self.is_severe(),
        }


@dataclass
class TimeSensitivity:
    """Time-sensitive factor affecting when something must happen."""

    id: str
    name: str  # "service_deadline", "cure_period", "notice_period", "response_deadline"
    trigger_event: str  # What starts the clock
    duration_days: int
    duration_hours: int = 0
    weather_dependent: bool = False  # Does weather pause the clock?
    holiday_dependent: bool = False  # Do holidays pause the clock?
    jurisdiction: str = "US"
    calendar_alert_days: int = 3  # Alert N days before deadline
    description: str = ""

    def get_deadline(self, start_date: datetime) -> datetime:
        """Calculate deadline from start date."""
        return start_date + timedelta(days=self.duration_days, hours=self.duration_hours)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class WeatherManager:
    """Manages weather data and integrations."""

    def __init__(self):
        self.cache_file = WEATHER_DIR / "weather_cache.json"
        self.conditions: Dict[str, WeatherCondition] = {}
        self.load()

    def add_weather_condition(
        self,
        date: datetime,
        location: str,
        temperature_f: float,
        condition: str,
        humidity_percent: int = 50,
        wind_speed_mph: float = 0,
        precipitation_inches: float = 0,
        visibility_miles: float = 10,
        alerts: Optional[List[str]] = None,
        source: str = "manual",
    ) -> WeatherCondition:
        """Add or update weather data for a date/location.

        Args:
            date: Date of weather
            location: Address or coordinate string
            temperature_f: Temperature in Fahrenheit
            condition: Weather condition type
            humidity_percent: Humidity %
            wind_speed_mph: Wind speed
            precipitation_inches: Rain/snow inches
            visibility_miles: Visibility distance
            alerts: Weather alerts in effect
            source: Data source

        Returns: WeatherCondition object
        """
        with _weather_lock:
            key = f"{date.date().isoformat()}_{location}"
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
            self.conditions[key] = weather
            self._persist()
            return weather

    def get_weather(
        self, date: datetime, location: str
    ) -> Optional[WeatherCondition]:
        """Get weather for specific date/location."""
        with _weather_lock:
            key = f"{date.date().isoformat()}_{location}"
            return self.conditions.get(key)

    def get_weather_for_period(
        self, start_date: datetime, end_date: datetime, location: str
    ) -> List[WeatherCondition]:
        """Get weather for date range at location."""
        with _weather_lock:
            results = []
            current = start_date
            while current <= end_date:
                key = f"{current.date().isoformat()}_{location}"
                if key in self.conditions:
                    results.append(self.conditions[key])
                current += timedelta(days=1)
            return results

    def has_severe_weather(
        self, start_date: datetime, end_date: datetime, location: str
    ) -> bool:
        """Check if period has severe weather."""
        with _weather_lock:
            conditions = self.get_weather_for_period(start_date, end_date, location)
            return any(c.is_severe() for c in conditions)

    def load(self):
        """Load cached weather from disk."""
        with _weather_lock:
            if self.cache_file.exists():
                try:
                    data = json.loads(self.cache_file.read_text())
                    for key, item in data.items():
                        self.conditions[key] = WeatherCondition(
                            date=datetime.fromisoformat(item["date"]),
                            location=item["location"],
                            temperature_f=item["temperature_f"],
                            condition=item["condition"],
                            humidity_percent=item["humidity_percent"],
                            wind_speed_mph=item["wind_speed_mph"],
                            precipitation_inches=item["precipitation_inches"],
                            visibility_miles=item["visibility_miles"],
                            alerts=item["alerts"],
                            source=item["source"],
                            cached_at=datetime.fromisoformat(item["cached_at"]),
                        )
                except Exception as e:
                    print(f"Error loading weather cache: {e}")

    def _persist(self):
        """Save weather cache to disk."""
        with _weather_lock:
            data = {k: v.to_dict() for k, v in self.conditions.items()}
            self.cache_file.write_text(json.dumps(data, indent=2))


class TimeSensitivityManager:
    """Manages time-sensitive business logic and deadlines."""

    def __init__(self):
        self.file = WEATHER_DIR / "time_sensitivities.json"
        self.sensitivities: Dict[str, TimeSensitivity] = {}
        self._initialize_default_sensitivities()
        self.load()

    def _initialize_default_sensitivities(self):
        """Set up standard legal time sensitivities."""
        import uuid

        defaults = [
            TimeSensitivity(
                id=str(uuid.uuid4()),
                name="eviction_notice_period",
                trigger_event="notice_served",
                duration_days=3,
                weather_dependent=False,
                holiday_dependent=True,
                description="Notice must be served 3+ days before eviction",
            ),
            TimeSensitivity(
                id=str(uuid.uuid4()),
                name="cure_period",
                trigger_event="notice_issued",
                duration_days=5,
                weather_dependent=False,
                holiday_dependent=True,
                description="Tenant has 5 days to cure after notice",
            ),
            TimeSensitivity(
                id=str(uuid.uuid4()),
                name="service_deadline",
                trigger_event="filing_date",
                duration_days=90,
                weather_dependent=True,
                holiday_dependent=False,
                description="Defendant must be served within 90 days (paused for severe weather)",
            ),
            TimeSensitivity(
                id=str(uuid.uuid4()),
                name="response_deadline",
                trigger_event="service_completed",
                duration_days=20,
                weather_dependent=False,
                holiday_dependent=True,
                description="Defendant has 20 days to respond",
            ),
            TimeSensitivity(
                id=str(uuid.uuid4()),
                name="security_deposit_return",
                trigger_event="lease_ended",
                duration_days=30,
                weather_dependent=False,
                holiday_dependent=False,
                description="Security deposit must be returned within 30 days",
            ),
        ]

        for sens in defaults:
            if sens.name not in self.sensitivities:
                self.sensitivities[sens.name] = sens

    def get_sensitivity(self, name: str) -> Optional[TimeSensitivity]:
        """Get sensitivity by name."""
        with _weather_lock:
            return self.sensitivities.get(name)

    def calculate_deadline(
        self,
        sensitivity_name: str,
        start_date: datetime,
        location: Optional[str] = None,
        weather_manager: Optional["WeatherManager"] = None,
    ) -> Dict[str, Any]:
        """Calculate deadline accounting for weather, holidays, etc.

        Args:
            sensitivity_name: Which time sensitivity applies
            start_date: When the clock starts
            location: For weather-dependent calculations
            weather_manager: Weather manager for checking conditions

        Returns: Dict with deadline, adjustments, and notes
        """
        with _weather_lock:
            sens = self.sensitivities.get(sensitivity_name)
            if not sens:
                return {"error": f"Unknown sensitivity: {sensitivity_name}"}

            deadline = sens.get_deadline(start_date)
            adjustments = []

            # Check for severe weather delays
            if sens.weather_dependent and weather_manager and location:
                severe_days = 0
                current = start_date
                while current <= deadline:
                    weather = weather_manager.get_weather(current, location)
                    if weather and weather.is_severe():
                        severe_days += 1
                        adjustments.append(
                            {
                                "type": "severe_weather",
                                "date": current.isoformat(),
                                "condition": weather.condition,
                            }
                        )
                    current += timedelta(days=1)

                if severe_days > 0:
                    deadline += timedelta(days=severe_days)
                    adjustments.append(
                        {
                            "type": "deadline_extension",
                            "reason": "severe_weather",
                            "days": severe_days,
                        }
                    )

            return {
                "sensitivity": sensitivity_name,
                "start_date": start_date.isoformat(),
                "deadline": deadline.isoformat(),
                "duration_days": sens.duration_days,
                "days_remaining": (deadline.date() - datetime.now().date()).days,
                "location": location,
                "adjustments": adjustments,
                "notes": sens.description,
            }

    def load(self):
        """Load from persistent storage."""
        with _weather_lock:
            if self.file.exists():
                try:
                    data = json.loads(self.file.read_text())
                    for item in data:
                        self.sensitivities[item["name"]] = TimeSensitivity(**item)
                except Exception as e:
                    print(f"Error loading time sensitivities: {e}")

    def _persist(self):
        """Save to persistent storage."""
        with _weather_lock:
            data = [s.to_dict() for s in self.sensitivities.values()]
            self.file.write_text(json.dumps(data, indent=2))


# Global instances
_weather_manager: Optional[WeatherManager] = None
_time_sensitivity_manager: Optional[TimeSensitivityManager] = None


def get_weather_manager() -> WeatherManager:
    """Get or create weather manager."""
    global _weather_manager
    if _weather_manager is None:
        _weather_manager = WeatherManager()
    return _weather_manager


def get_time_sensitivity_manager() -> TimeSensitivityManager:
    """Get or create time sensitivity manager."""
    global _time_sensitivity_manager
    if _time_sensitivity_manager is None:
        _time_sensitivity_manager = TimeSensitivityManager()
    return _time_sensitivity_manager
