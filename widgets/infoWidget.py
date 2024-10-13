
from PyQt5 import QtCore, QtWidgets

from core.config import *


class InfoWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        
        self.setObjectName('infoWidget')

        layout = QtWidgets.QVBoxLayout(self)

        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(0)

        appNameLabel = QtWidgets.QLabel(parent=self, text=f'{APPLICATION_NAME.upper()}')
        appNameLabel.setObjectName('appNameLabel')
        appNameLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(appNameLabel)

        appDescriptionLabel = QtWidgets.QLabel(parent=self, text=f'VERSION {APPLICATION_VERSION}')
        appDescriptionLabel.setObjectName('appDescriptionLabel')
        appDescriptionLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(appDescriptionLabel)
