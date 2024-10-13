
import json
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

import requests
from requests.exceptions import RequestException

from .utils import resource
from .exceptions import eprint, LocationServerError


@dataclass
class LocationData:
    country: str
    city: str
    lat: float
    lon: float


class LocationService(ABC):
    '''Interface to get location data from any service'''

    @abstractmethod
    def get(self) -> LocationData:
        raise NotImplementedError


class IpInfoLocationService(LocationService):

    def get(self) -> LocationData:
        '''get current location by ip'''

        try:
            response = requests.get('https://ipinfo.io/')
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

        #
        logger = logging.getLogger('app')
        logger.info(f'Location: {city}, {country}')

        #
        return LocationData(
            country=country,
            city=city,
            lat=lat,
            lon=lon,
        )
