
import json
import logging
import os
from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
import requests
from requests.exceptions import RequestException
import datetime
from .config import FORECAST_DAYS_SPAN, FORECAST_HOUR_PERIOD, LOCATION, API_KEY
from .utils import resource
from .exceptions import eprint, WeatherServerError
import calendar


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
    midday_icon: str
    max_day_pop: str


@dataclass
class WeatherData:
    flag: bool
    current: WeatherDataCurrent
    forecast: tuple[WeatherDataForecast]


class OpenWeatherMapWeatherService:
    @classmethod
    def from_dict(cls, data: Mapping) -> WeatherData:
        return WeatherData(
            flag=data['flag'],
            current=WeatherDataCurrent(**data),
            forecast=tuple(WeatherDataForecast(**datum)
                           for datum in data['forecast']),
        )

    def get(self) -> WeatherData:
        try:
            exclude = ','.join(['minutely', 'hourly', 'alerts'])
            units = 'metric'
            url = f'https://api.openweathermap.org/data/2.5/weather?lat={LOCATION.lat}&lon={
                LOCATION.lon}&units={units}&exclude={exclude}&appid={API_KEY}'

            response = requests.get(url)

            if response.status_code == 200:
                flag = True
                weatherData = response.json()

                filename = os.path.join('.', '.weather.json')
                with open(resource(filename), 'w') as file:
                    json.dump(weatherData, file)

            else:
                raise WeatherServerError()

            url = f'https://api.openweathermap.org/data/2.5/forecast?lat={LOCATION.lat}&lon={
                LOCATION.lon}&units={units}&exclude={exclude}&appid={API_KEY}'

            response = requests.get(url)

            if response.status_code == 200:
                flag = True
                forecastData = response.json()

                filename = os.path.join('.', '.forecast.json')
                with open(resource(filename), 'w') as file:
                    json.dump(forecastData, file)
            else:
                raise WeatherServerError()

        except (RequestException, WeatherServerError) as error:
            eprint(error)

            filename = os.path.join('.', '.weather.json')
            if os.path.exists(resource(filename)):
                with open(resource(filename), 'r') as file:
                    weatherData = json.load(file)
            else:
                weatherData = {}

            filename = os.path.join('.', '.forecast.json')
            if os.path.exists(resource(filename)):
                with open(resource(filename), 'r') as file:
                    forecastData = json.load(file)
            else:
                forecastData = {}
            flag = False

        current = WeatherDataCurrent(
            icon=weatherData['weather'][0]['icon'],
            t=weatherData['main']['temp'],
            t_feels_like=weatherData['main']['feels_like'],
            description=weatherData['weather'][0]['description'],
            dt=datetime.datetime.fromtimestamp(
                weatherData['dt']).strftime('%H:%M %d/%m')
        )

        forecastProcessed = self.process_forecast_data(forecastData)

        forecast = tuple([
            WeatherDataForecast(
                date=datum['date'],
                weekday=datum['weekday'],
                temp_min=datum['day_min'],
                temp_max=datum['day_max'],
                midday_icon=datum['midday_icon'],
                max_day_pop=datum['max_day_pop']
            )
            for datum in forecastProcessed
        ])

        logger = logging.getLogger('app')
        logger.info('Weather: {}'.format(
            f'Weather: {current}' if flag else 'Weather: service error!',
        ))

        return WeatherData(
            flag=flag,
            current=current,
            forecast=forecast,
        )

    def process_forecast_data(self, data):
        weather_list = data['list']
        result = []
        for dayInfo in weather_list:
            date = datetime.datetime.fromtimestamp(dayInfo['dt'])
            result.append({
                'date': date.strftime('%d/%m'),
                'datetime': dayInfo['dt_txt'],
                'weekday': calendar.day_name[date.weekday()],
                'temp_min': dayInfo['main']['temp_min'],
                'temp_max': dayInfo['main']['temp_max'],
                'icon': dayInfo['weather'][0]['icon'],
                'pop': dayInfo['pop']
            })

        groupedForecast = self.group_day_forecast(result)

        return [{
            'date': day[0]['date'],
            'weekday': day[0]['weekday'],
            'day_min': min([value['temp_min'] for value in day]),
            'day_max': max([value['temp_min'] for value in day]),
            'midday_icon': day[12//FORECAST_HOUR_PERIOD]['icon'],
            'max_day_pop': max([value['pop'] for value in day])
        }
            for day in groupedForecast
        ]

    def group_day_forecast(self, forecastList: list):
        grouped_data = []
        for obj in forecastList:
            if len(grouped_data) == 0:
                grouped_data.append([obj])
            else:
                if obj['date'] == grouped_data[-1][0]['date']:
                    grouped_data[-1].append(obj)
                else:
                    grouped_data.append([obj])
        if len(grouped_data) == FORECAST_DAYS_SPAN + 1:
            grouped_data = grouped_data[1:]
        return grouped_data[:-1]
