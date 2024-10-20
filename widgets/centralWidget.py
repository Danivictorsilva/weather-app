
from PyQt5 import QtWidgets
from contracts.contracts import *
from core.config import *
from widgets.weatherWidget import WeatherWidget
from widgets.locationWidget import LocationWidget
from widgets.infoWidget import InfoWidget


class CentralWidget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        layout.addWidget(LocationWidget())
        layout.addWidget(WeatherWidget())
        layout.addWidget(InfoWidget())

    def update(self, data: LocAndWeatherPayload):
        todayWeatherWidget = self.findChild(
            QtWidgets.QWidget, 'todayWeatherWidget')
        todayWeatherWidget.update(data.weather_data)

        locationWidget = self.findChild(QtWidgets.QWidget, 'locationWidget')
        locationWidget.update(data.location_data)
