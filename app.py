
import logging
import sys

from PyQt5 import QtCore, QtWidgets

from core.config import *
from core.style import load_style
from core.weather import WeatherData, OpenWeatherMapWeatherService
from widgets.todayWeatherWidget import TodayWeatherWidget
from widgets.locationWidget import LocationWidget
from widgets.infoWidget import InfoWidget


weather_service = OpenWeatherMapWeatherService()

class UpdateWeatherThread(QtCore.QThread):
    updated = QtCore.pyqtSignal(WeatherData)

    def __init__(self):
        super().__init__()

    def run(self):
        data = weather_service.get()
        self.updated.emit(data)


class CentralWidget(QtWidgets.QFrame):

    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)

        layout.addWidget(LocationWidget())
        layout.addWidget(TodayWeatherWidget())
        layout.addWidget(InfoWidget())

    def update(self, data: WeatherData):
        widget = self.findChild(QtWidgets.QWidget, 'todayWeatherWidget')
        widget.update(data)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, flags):
        super().__init__(flags=flags)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        # icon
        # icon = QtGui.QIcon(resource('icon.ico'))
        # self.setWindowIcon(icon)

        style = load_style()
        self.setStyleSheet(style)

        self.centralWidget = CentralWidget()
        self.setCentralWidget(self.centralWidget)

        # update weather thread
        self.updateWeatherThread = UpdateWeatherThread()
        self.updateWeatherThread.updated.connect(self.centralWidget.update)

        # update weather timer
        self.updateWeatherTimer = QtCore.QTimer()
        self.updateWeatherTimer.setInterval(WEATHER_UPDATE_INTERVAL)
        self.updateWeatherTimer.timeout.connect(self.updateWeatherThread.start)
        self.updateWeatherTimer.start()

        # first shot
        QtCore.QTimer.singleShot(300, self.updateWeatherThread.start)

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


if __name__ == '__main__':

    if DEBUG:
        logger = logging.getLogger('app')
        logger.debug('app: run.')

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(
        flags=QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint,
    )

    window.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing window...')
