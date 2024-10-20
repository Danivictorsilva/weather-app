
from dataclasses import dataclass
from PyQt5 import  QtWidgets
from core.config import *
from core.location import LocationData
from core.weather import WeatherData
from widgets.todayWeatherWidget import TodayWeatherWidget
from widgets.locationWidget import LocationWidget
from widgets.infoWidget import InfoWidget

@dataclass
class LocAndWeatherPayload:
    location_data: LocationData
    weather_data: WeatherData

class CentralWidget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        layout.addWidget(LocationWidget())
        layout.addWidget(TodayWeatherWidget())
        layout.addWidget(InfoWidget())

    def update(self, data: LocAndWeatherPayload):
        todayWeatherWidget = self.findChild(QtWidgets.QWidget, 'todayWeatherWidget')
        todayWeatherWidget.update(data.weather_data)

        locationWidget = self.findChild(QtWidgets.QWidget, 'locationWidget')
        locationWidget.update(data.location_data)
    
