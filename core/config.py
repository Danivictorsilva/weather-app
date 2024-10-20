
import logging
import logging.config
import os

from .utils import resource

DEBUG = True

# --------        LOGGING        --------
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'stream_formatter': {
            'format': '[%(asctime)s: %(levelname)s] %(message)s',
        },
        'file_formatter': {
            'format': '[%(asctime)s: %(levelname)s] %(message)s',
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG,
            'formatter': 'stream_formatter',
        },
        'file_handler': {
            'class': 'logging.FileHandler',
            'level': logging.INFO,
            'filename': os.path.join('.', 'app.log'),
            'mode': 'a',
            'formatter': 'file_formatter',
        },
    },

    'loggers': {
        'app': {
            'level': logging.DEBUG,
            'handlers': ['stream_handler', 'file_handler'],
            'propagate': True,
        },
    },

}
)

# --------        ENV        --------
filepath = '.env'
with open(resource(filepath), mode='r') as file:
    for line in file.readlines():
        key, value = line.split('=')

        os.environ[key] = value

API_KEY = os.environ['API_KEY']

# --------        APP        --------
APPLICATION_NAME = 'Weather App'
APPLICATION_VERSION = '1.0.0'
IPINFO_URL = 'https://ipinfo.io/'
OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/'
WEATHER_URL = OPENWEATHER_BASE_URL + 'data/2.5/weather'
FORECAST_URL = OPENWEATHER_BASE_URL + 'data/2.5/forecast'
GEOLOCAL_URL = OPENWEATHER_BASE_URL + 'geo/1.0/direct'

# --------        WEATHER        --------
WEATHER_UPDATE_INTERVAL = 10 * 60 * 1000  # time, in msec
FORECAST_DAYS_SPAN = 5
FORECAST_HOUR_PERIOD = 3
EXCLUDE = ','.join(['minutely', 'hourly', 'alerts'])
UNITS = 'metric'
