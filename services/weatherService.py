
import json
import logging
import os
import datetime
import requests
import calendar
from requests.exceptions import RequestException
from contracts.contracts import *
from core.config import *
from core.utils import resource
from core.exceptions import eprint, WeatherServerError


class WeatherService:
    def get(self, location: LocationData) -> WeatherData:
        '''Get weather info from a given location.'''
        try:
            response = requests.get(
                f'{WEATHER_URL}?lat={location.lat}&lon={location.lon}&units={
                    UNITS}&exclude={EXCLUDE}&appid={API_KEY}'
            )

            if response.status_code == 200:
                flag = True
                weather_data = response.json()
                filename = os.path.join('.', '.weather.json')
                with open(resource(filename), 'w') as file:
                    json.dump(weather_data, file)
            else:
                raise WeatherServerError()

            response = requests.get(
                f'{FORECAST_URL}?lat={location.lat}&lon={location.lon}&units={
                    UNITS}&exclude={EXCLUDE}&appid={API_KEY}'
            )

            if response.status_code == 200:
                flag = True
                forecast_data = response.json()
                filename = os.path.join('.', '.forecast.json')
                with open(resource(filename), 'w') as file:
                    json.dump(forecast_data, file)
            else:
                raise WeatherServerError()

        except (RequestException, WeatherServerError) as error:
            flag = False
            eprint(error)
            filename = os.path.join('.', '.weather.json')
            if os.path.exists(resource(filename)):
                with open(resource(filename), 'r') as file:
                    weather_data = json.load(file)
            else:
                weather_data = {}

            filename = os.path.join('.', '.forecast.json')
            if os.path.exists(resource(filename)):
                with open(resource(filename), 'r') as file:
                    forecast_data = json.load(file)
            else:
                forecast_data = {}

        current = self.process_current_weather_data(weather_data)
        forecast = self.process_forecast_data(forecast_data)

        logger = logging.getLogger('app')
        logger.info('Weather: {}'.format(
            f'Weather: {current}' if flag else 'Weather: service error!',
        ))

        return WeatherData(
            flag=flag,
            current=current,
            forecast=tuple(forecast),
        )

    def process_current_weather_data(self, data) -> WeatherDataCurrent:
        '''Process raw api weather response to WeatherDataCurrent.'''
        return WeatherDataCurrent(
            icon=data['weather'][0]['icon'],
            t=data['main']['temp'],
            t_feels_like=data['main']['feels_like'],
            description=data['weather'][0]['description'],
            dt=datetime.datetime.fromtimestamp(
                data['dt']).strftime('%H:%M %d/%m')
        )

    def process_forecast_data(self, data) -> list[WeatherDataForecast]:
        '''Process raw api forecast response to WeatherDataForecast.'''
        weather_list = [
            dict(
                date=datetime.datetime.fromtimestamp(
                    dayInfo['dt']).strftime('%d/%m'),
                weekday=calendar.day_name[datetime.datetime.fromtimestamp(
                    dayInfo['dt']).weekday()],
                temp_min=dayInfo['main']['temp_min'],
                temp_max=dayInfo['main']['temp_max'],
                icon=dayInfo['weather'][0]['icon'],
                pop=dayInfo['pop'],
                datetime=dayInfo['dt_txt']
            )
            for dayInfo in data['list']
        ]

        grouped_forecast = self.group_day_forecast(weather_list)

        return [
            WeatherDataForecast(
                date=day[0]['date'],
                weekday=day[0]['weekday'],
                temp_min=min([float(item['temp_min']) for item in day]),
                temp_max=max([float(item['temp_max']) for item in day]),
                midday_icon=day[12 // FORECAST_HOUR_PERIOD]['icon'],
                max_day_pop=max([float(item['pop']) for item in day])
            )
            for day in grouped_forecast
        ]

    def group_day_forecast(self, forecast_list: list):
        '''Group forecast data by day. Return a list of compiled hourly forecast for the next (FORECAST_DAYS_SPAN - 1) days.'''
        grouped_data = []
        for item in forecast_list:
            if len(grouped_data) == 0:
                grouped_data.append([item])
            else:
                if item['date'] == grouped_data[-1][0]['date']:
                    grouped_data[-1].append(item)
                else:
                    grouped_data.append([item])

        if len(grouped_data) == FORECAST_DAYS_SPAN + 1:
            grouped_data = grouped_data[1:]

        return grouped_data[:-1]
