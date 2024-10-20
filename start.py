import logging
import sys
from PyQt5 import QtCore, QtWidgets
from core.config import DEBUG
from app import MainWindow

if __name__ == '__main__':
    if DEBUG:
        logger = logging.getLogger('app')
        logger.debug('app: run.')

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(flags=QtCore.Qt.Window |
                        QtCore.Qt.WindowStaysOnTopHint)
    window.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing window...')
