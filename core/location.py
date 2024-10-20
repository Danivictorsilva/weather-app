import json
import logging
import os
from dataclasses import dataclass
import requests
from requests.exceptions import RequestException
from .utils import resource
from .exceptions import eprint, LocationServerError
from .config import API_KEY, GEOLOCAL_URL, IPINFO_URL


@dataclass
class LocationData:
    country: str
    city: str
    lat: float
    lon: float


class LocationService:
    def get_location(self) -> LocationData:
        return self.location

    def fetch_current(self) -> LocationData:
        '''Get current location by ip'''
        try:
            response = requests.get(IPINFO_URL)
            if response.status_code == 200:
                data = response.json()

                filename = os.path.join('.', '.location.json')
                with open(resource(filename), 'w') as file:
                    json.dump(data, file)

            else:
                raise LocationServerError()

        except (LocationServerError, RequestException) as error:
            eprint(error)

            filename = os.path.join('.', '.location.json')
            if os.path.exists(resource(filename)):
                with open(resource(filename), 'r') as file:
                    data = json.load(file)

            else:
                data = {
                    'city': 'S\u00e3o Paulo',
                    'country': 'BR',
                    'loc': '-23.5475,-46.6361'
                }

        country = data['country']
        city = data['city']
        lat, lon = map(float, data['loc'].split(','))

        logger = logging.getLogger('app')
        logger.info(f'Location: {city}, {country}')

        self.location = LocationData(
            country=country,
            city=city,
            lat=lat,
            lon=lon,
        )
        return self.location

    def fetch_by_city(self, city: str) -> LocationData:
        '''Get current location by inserted location'''
        try:
            response = requests.get(
                f'{GEOLOCAL_URL}?q={city}&limit=1&appid={API_KEY}')

            if response.status_code == 200 and len(response.json()) != 0:
                data = response.json()
            else:
                raise LocationServerError()

        except (LocationServerError, RequestException) as error:
            eprint(error)
            data = [{
                    'name': 'Location not found',
                    'country': 'try again',
                    'lat': '-23.5475',
                    'lon': '-46.6361'
                    }]

        country = data[0]['country']
        city = data[0]['name']
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])

        self.location = LocationData(
            country=country,
            city=city,
            lat=lat,
            lon=lon,
        )
        return self.location
