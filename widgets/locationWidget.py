
from PyQt5 import QtCore, QtWidgets

from core.location import LocationData


class LocationWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName('locationWidget')

        layout = QtWidgets.QVBoxLayout(self)

        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(0)

        locationLabel = QtWidgets.QLabel(text=f'', parent=self)
        locationLabel.setObjectName('locationLabel')
        locationLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(locationLabel)

    def update(self, data: LocationData):
        locationLabel = self.findChild(QtWidgets.QLabel, 'locationLabel')
        locationLabel.setText(
            f'{data.city}, {data.country}'
        )
