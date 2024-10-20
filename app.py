from PyQt5 import QtCore, QtWidgets
from core.config import WEATHER_UPDATE_INTERVAL
from core.location import LocationService
from core.style import load_style
from core.weather import OpenWeatherService
from widgets.centralWidget import CentralWidget, LocAndWeatherPayload

location_service = LocationService()
location_service.fetch_current()
weather_service = OpenWeatherService()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, flags):
        super().__init__(flags=flags)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        style = load_style()
        self.setStyleSheet(style)

        self.centralWidget = CentralWidget()
        self.setCentralWidget(self.centralWidget)

        button_layout = QtWidgets.QHBoxLayout()
        self.myLocationButton = QtWidgets.QPushButton("My Location", self)
        self.searchCityButton = QtWidgets.QPushButton("Search City", self)

        self.myLocationButton.clicked.connect(
            self.update_weather_with_ip_location)
        self.searchCityButton.clicked.connect(self.search_city_weather)

        button_layout.addWidget(self.myLocationButton)
        button_layout.addWidget(self.searchCityButton)

        layout: QtWidgets.QVBoxLayout = self.centralWidget.layout()
        layout.insertLayout(0, button_layout)

        self.updateWeatherThread = UpdateWeatherThread()
        self.updateWeatherThread.updated.connect(self.centralWidget.update)

        self.updateWeatherTimer = QtCore.QTimer()
        self.updateWeatherTimer.setInterval(WEATHER_UPDATE_INTERVAL)
        self.updateWeatherTimer.timeout.connect(self.updateWeatherThread.start)
        self.updateWeatherTimer.start()

        QtCore.QTimer.singleShot(300, self.updateWeatherThread.start)

    def update_weather_with_ip_location(self):
        location_service.fetch_current()
        self.updateWeatherThread.start()

    def search_city_weather(self):
        dialog = QtWidgets.QInputDialog(self)
        dialog.setWindowTitle('Search City')
        dialog.setLabelText('Enter city name:')
        dialog.setOkButtonText('Search')
        dialog.setCancelButtonText('Cancel')

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            city = dialog.textValue()
            if city:
                location_service.fetch_by_city(city)
                self.updateWeatherThread.start()

    # used to move frameless window
    def mousePressEvent(self, event):
        self._beginPos = event.globalPos()

    # used to move frameless window
    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self._beginPos)
        self.move(
            self.x() + delta.x(),
            self.y() + delta.y(),
        )
        self._beginPos = event.globalPos()


class UpdateWeatherThread(QtCore.QThread):
    updated = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()

    def run(self):
        location = location_service.get_location()
        self.updated.emit(
            LocAndWeatherPayload(
                location_data=location,
                weather_data=weather_service.get(location)
            ))
