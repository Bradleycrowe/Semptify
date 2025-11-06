"""
Weather and Time Sensitivity Management Module

Provides weather tracking and time-sensitive deadline calculations.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import uuid


@dataclass
class WeatherCondition:
    """Weather condition for a specific date and location."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    date: datetime = field(default_factory=datetime.now)
    location: str = ""
    temperature_f: float = 70.0
    condition: str = "clear"
    humidity_percent: float = 50.0
    wind_speed_mph: float = 0.0
    precipitation_inches: float = 0.0
    visibility_miles: float = 10.0
    alerts: List[str] = field(default_factory=list)
    source: str = "manual"
    
    def to_dict(self) -> dict:
        """Convert weather condition to dictionary."""
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "location": self.location,
            "temperature_f": self.temperature_f,
            "condition": self.condition,
            "humidity_percent": self.humidity_percent,
            "wind_speed_mph": self.wind_speed_mph,
            "precipitation_inches": self.precipitation_inches,
            "visibility_miles": self.visibility_miles,
            "alerts": self.alerts,
            "source": self.source
        }
    
    def is_severe(self) -> bool:
        """Check if weather is severe."""
        severe_conditions = ["thunderstorm", "tornado", "hurricane", "blizzard", "ice"]
        return (
            self.condition.lower() in severe_conditions or
            len(self.alerts) > 0 or
            self.wind_speed_mph > 40 or
            self.precipitation_inches > 2.0 or
            self.visibility_miles < 1.0
        )


class WeatherManager:
    """Manages weather conditions and caching."""
    
    def __init__(self):
        self.conditions: List[WeatherCondition] = []
    
    def add_weather_condition(
        self,
        date: datetime,
        location: str,
        temperature_f: float,
        condition: str,
        humidity_percent: float = 50.0,
        wind_speed_mph: float = 0.0,
        precipitation_inches: float = 0.0,
        visibility_miles: float = 10.0,
        alerts: Optional[List[str]] = None,
        source: str = "api"
    ) -> WeatherCondition:
        """Add or update weather for a date/location."""
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
            source=source
        )
        
        # Remove existing entry for same date/location
        self.conditions = [
            c for c in self.conditions
            if not (c.date.date() == date.date() and c.location == location)
        ]
        
        self.conditions.append(weather)
        return weather
    
    def get_weather(
        self,
        date: datetime,
        location: str
    ) -> Optional[WeatherCondition]:
        """Get weather for specific date and location."""
        for condition in self.conditions:
            if condition.date.date() == date.date() and condition.location == location:
                return condition
        return None
    
    def get_weather_for_period(
        self,
        start_date: datetime,
        end_date: datetime,
        location: str
    ) -> List[WeatherCondition]:
        """Get weather for a date range."""
        return [
            c for c in self.conditions
            if (
                c.location == location and
                start_date.date() <= c.date.date() <= end_date.date()
            )
        ]
    
    def has_severe_weather(
        self,
        start_date: datetime,
        end_date: datetime,
        location: str
    ) -> bool:
        """Check if there was severe weather in period."""
        conditions = self.get_weather_for_period(start_date, end_date, location)
        return any(c.is_severe() for c in conditions)


@dataclass
class TimeSensitivity:
    """Time sensitivity definition for calculating deadlines."""
    
    name: str = ""
    description: str = ""
    base_days: int = 30
    exclude_weekends: bool = True
    exclude_holidays: bool = True
    weather_extension_days: int = 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "base_days": self.base_days,
            "exclude_weekends": self.exclude_weekends,
            "exclude_holidays": self.exclude_holidays,
            "weather_extension_days": self.weather_extension_days
        }


class TimeSensitivityManager:
    """Manages time sensitivities and deadline calculations."""
    
    def __init__(self):
        self.sensitivities: Dict[str, TimeSensitivity] = {}
        self._initialize_defaults()
    
    def _initialize_defaults(self):
        """Initialize default time sensitivities."""
        self.sensitivities["service_deadline"] = TimeSensitivity(
            name="service_deadline",
            description="Deadline for serving legal documents",
            base_days=20,
            exclude_weekends=True,
            exclude_holidays=True,
            weather_extension_days=3
        )
        
        self.sensitivities["response_deadline"] = TimeSensitivity(
            name="response_deadline",
            description="Deadline for filing a response",
            base_days=30,
            exclude_weekends=True,
            exclude_holidays=True,
            weather_extension_days=0
        )
        
        self.sensitivities["appeal_deadline"] = TimeSensitivity(
            name="appeal_deadline",
            description="Deadline for filing an appeal",
            base_days=60,
            exclude_weekends=True,
            exclude_holidays=True,
            weather_extension_days=0
        )
    
    def add_sensitivity(self, sensitivity: TimeSensitivity):
        """Add or update a time sensitivity."""
        self.sensitivities[sensitivity.name] = sensitivity
    
    def calculate_deadline(
        self,
        sensitivity_name: str,
        start_date: datetime,
        location: Optional[str] = None,
        weather_manager: Optional[WeatherManager] = None
    ) -> dict:
        """Calculate deadline with weather/sensitivity adjustments."""
        if sensitivity_name not in self.sensitivities:
            return {
                "error": f"Unknown sensitivity: {sensitivity_name}",
                "available": list(self.sensitivities.keys())
            }
        
        sensitivity = self.sensitivities[sensitivity_name]
        current_date = start_date
        days_added = 0
        business_days_added = 0
        
        while business_days_added < sensitivity.base_days:
            current_date += timedelta(days=1)
            days_added += 1
            
            # Skip weekends if required
            if sensitivity.exclude_weekends and current_date.weekday() >= 5:
                continue
            
            business_days_added += 1
        
        # Check for severe weather and extend if needed
        weather_extension = 0
        if location and weather_manager and sensitivity.weather_extension_days > 0:
            if weather_manager.has_severe_weather(start_date, current_date, location):
                weather_extension = sensitivity.weather_extension_days
                current_date += timedelta(days=weather_extension)
        
        return {
            "sensitivity": sensitivity_name,
            "start_date": start_date.isoformat(),
            "deadline": current_date.isoformat(),
            "base_days": sensitivity.base_days,
            "calendar_days": days_added + weather_extension,
            "weather_extension_days": weather_extension,
            "exclude_weekends": sensitivity.exclude_weekends,
            "exclude_holidays": sensitivity.exclude_holidays
        }


# Singleton instances
_weather_manager: Optional[WeatherManager] = None
_time_sensitivity_manager: Optional[TimeSensitivityManager] = None


def get_weather_manager() -> WeatherManager:
    """Get the weather manager singleton."""
    global _weather_manager
    if _weather_manager is None:
        _weather_manager = WeatherManager()
    return _weather_manager


def get_time_sensitivity_manager() -> TimeSensitivityManager:
    """Get the time sensitivity manager singleton."""
    global _time_sensitivity_manager
    if _time_sensitivity_manager is None:
        _time_sensitivity_manager = TimeSensitivityManager()
    return _time_sensitivity_manager
