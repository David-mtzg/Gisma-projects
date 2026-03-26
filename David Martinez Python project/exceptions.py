"""

Custom exception hierarchy for the Weather Dashboard.

"""

from typing import Optional


class WeatherDashboardError(Exception):
    """Base exception for all application errors."""


class APIError(WeatherDashboardError):
    """Raised when an external API call fails."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self) -> str:
        if self.status_code:
            return f"APIError [{self.status_code}]: {super().__str__()}"
        return f"APIError: {super().__str__()}"


class CityNotFoundError(WeatherDashboardError):
    """Raised when a city cannot be geo-coded."""

    def __init__(self, city_name: str):
        super().__init__(f"City not found: '{city_name}'")
        self.city_name = city_name


class FileStorageError(WeatherDashboardError):
    """Raised on file read / write failures."""


class InvalidInputError(WeatherDashboardError):
    """Raised on bad user input."""