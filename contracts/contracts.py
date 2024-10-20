from dataclasses import dataclass


@dataclass
class LocationData:
    country: str
    city: str
    lat: float
    lon: float


@dataclass
class WeatherDataCurrent:
    icon: str | None
    t: float
    t_feels_like: float
    description: str
    dt: str

    def __str__(self) -> str:
        return f'{self.icon}, {self.t}, C'


@dataclass
class WeatherDataForecast:
    date: str
    weekday: str
    temp_min: float
    temp_max: float
    midday_icon: str | None
    max_day_pop: float


@dataclass
class WeatherData:
    flag: bool
    current: WeatherDataCurrent
    forecast: tuple[WeatherDataForecast]


@dataclass
class LocAndWeatherPayload:
    location_data: LocationData
    weather_data: WeatherData
