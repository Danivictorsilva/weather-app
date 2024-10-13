
import os
import re

from PyQt5 import QtCore, QtGui, QtWidgets

from core.config import FORECAST_DAYS_SPAN
from core.style import load_style
from core.weather import WeatherData, WeatherDataCurrent, WeatherDataForecast


class CurrentWeatherFrame(QtWidgets.QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName('currentWeatherFrame')

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        iconLabel = QtWidgets.QLabel(text=f'', parent=self)
        iconLabel.setObjectName('iconLabel')
        iconLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(iconLabel)

        descriptionLabel = QtWidgets.QLabel(text=f'', parent=self)
        descriptionLabel.setObjectName('descriptionLabel')
        descriptionLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(descriptionLabel)

        temperatureLabel = QtWidgets.QLabel(text=f'', parent=self)
        temperatureLabel.setObjectName('temperatureLabel')
        temperatureLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(temperatureLabel)

        feelsLikeLabel = QtWidgets.QLabel(text=f'', parent=self)
        feelsLikeLabel.setObjectName('feelsLikeLabel')
        feelsLikeLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(feelsLikeLabel)

        lastUpdatedLabel = QtWidgets.QLabel(text='', parent=self)
        lastUpdatedLabel.setObjectName('lastUpdatedLabel')
        lastUpdatedLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(lastUpdatedLabel)

    def update(self, data: WeatherDataCurrent, flag: bool):

        if data.icon is not None:
            filename = os.path.join('.', 'icons', data.icon + '@4x.png')
            pixmap = QtGui.QPixmap(filename)
            pixmap = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)

            iconLabel = self.findChild(QtWidgets.QLabel, 'iconLabel')
            iconLabel.setPixmap(pixmap)

        descriptionLabel = self.findChild(QtWidgets.QLabel, 'descriptionLabel')
        descriptionLabel.setText(
            f'<strong>{data.description.capitalize()}</strong>'
        )

        temperatureLabel = self.findChild(QtWidgets.QLabel, 'temperatureLabel')
        temperatureLabel.setText(
            f'<strong>{data.t:.0f}</strong> <span>&#8451;</span>'
        )

        feelsLikeLabel = self.findChild(QtWidgets.QLabel, 'feelsLikeLabel')
        feelsLikeLabel.setText(
            f'Feels like: <strong>{data.t_feels_like:.0f}</strong> <span>&#8451;</span>')

        lastUpdatedLabel = self.findChild(QtWidgets.QLabel, 'lastUpdatedLabel')
        lastUpdatedLabel.setText(f'Last updated: {data.dt}')


class ForecastWeatherFrame(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName('forecastWeatherFrame')
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSpacing(20)

        for day in range(1, FORECAST_DAYS_SPAN):
            frame = QtWidgets.QFrame(self)
            self.layout.addWidget(frame)
            layout = QtWidgets.QVBoxLayout(frame)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            weekdayLabel = QtWidgets.QLabel(text=f'', parent=self)
            weekdayLabel.setObjectName(f'{day}weekdayLabel')
            weekdayLabel.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            layout.addWidget(weekdayLabel)

            iconLabel = QtWidgets.QLabel(text=f'', parent=self)
            iconLabel.setObjectName(f'{day}iconLabel')
            iconLabel.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            layout.addWidget(iconLabel)

            maxTempLabel = QtWidgets.QLabel(text=f'', parent=self)
            maxTempLabel.setObjectName(f'{day}maxTempLabel')
            maxTempLabel.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            layout.addWidget(maxTempLabel)

            minTempLabel = QtWidgets.QLabel(text=f'', parent=self)
            minTempLabel.setObjectName(f'{day}minTempLabel')
            minTempLabel.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            layout.addWidget(minTempLabel)

            popLabel = QtWidgets.QLabel(text=f'', parent=self)
            popLabel.setObjectName(f'{day}popLabel')
            popLabel.setAlignment(
                QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            layout.addWidget(popLabel)

    def update(self, data: tuple[WeatherDataForecast], flag: bool):
        for day in range(1, FORECAST_DAYS_SPAN):
            dayInfo = data[day-1]

            weekdayLabel = self.findChild(
                QtWidgets.QLabel, f'{day}weekdayLabel')
            weekdayLabel.setText(
                f'<strong>{dayInfo.weekday.capitalize(
                )}</strong><br>{dayInfo.date}'
            )

            filename = os.path.join('.', 'icons', dayInfo.midday_icon + '.png')
            pixmap = QtGui.QPixmap(filename)

            iconLabel = self.findChild(QtWidgets.QLabel, f'{day}iconLabel')
            iconLabel.setPixmap(pixmap)

            maxTempLabel = self.findChild(
                QtWidgets.QLabel, f'{day}maxTempLabel')
            maxTempLabel.setText(
                f'Max: <strong>{
                    dayInfo.temp_max:.0f}</strong> <span>&#8451;</span>'
            )

            minTempLabel = self.findChild(
                QtWidgets.QLabel, f'{day}minTempLabel')
            minTempLabel.setText(
                f'Min: <strong>{
                    dayInfo.temp_min:.0f}</strong> <span>&#8451;</span>'
            )

            popLabel = self.findChild(QtWidgets.QLabel, f'{day}popLabel')
            popLabel.setText(f'Precipitation: <strong>{
                             f'{float(dayInfo.max_day_pop) * 100:.0f}'}</strong>%')


class TodayWeatherWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName('todayWeatherWidget')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 10, 0, 10)
        self.layout.setSpacing(20)
        self.layout.addWidget(CurrentWeatherFrame())
        self.layout.addWidget(ForecastWeatherFrame())

    def update(self, data: WeatherData):
        weatherWidget = self.findChild(QtWidgets.QFrame, 'currentWeatherFrame')
        weatherWidget.update(data.current, data.flag)

        forecastWidget = self.findChild(
            QtWidgets.QFrame, 'forecastWeatherFrame')
        forecastWidget.update(data.forecast, data.flag)
