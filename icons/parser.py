
import os

import requests

from .utils import resource


for icon_id in ['01', '02', '03', '04', '09', '10', '11', '13', '50']:
    for time_of_day in ['d', 'n']:
        for scale in ['', '@2x', '@4x']:
            url = f'https://openweathermap.org/img/wn/{icon_id}{time_of_day}{scale}.png'
            response = requests.get(url)

            filename = os.path.join('.', 'icons', f'{icon_id}{time_of_day}{scale}.png')
            with open(resource(filename), 'wb') as file:
                file.write(response.content)
