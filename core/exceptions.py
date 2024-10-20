
import sys
import traceback


class WeatherServerError(Exception):
    '''Weather server error.'''


class LocationServerError(Exception):
    '''LocationService server error.'''


def eprint(error: Exception) -> None:
    '''print exception traceback.'''
    traceback.print_exception(error, limit=2, file=sys.stdout)
