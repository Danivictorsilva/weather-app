
import os

from .exceptions import eprint
from .utils import resource


def load_style() -> dict:
    '''Import styles file.'''
    filepath = os.path.join('.', 'styles', 'app.css')
    try:
        with open(resource(filepath), mode='r') as file:
            style = file.read()
    except FileNotFoundError as error:
        style = ''
        eprint(error)

    return style
