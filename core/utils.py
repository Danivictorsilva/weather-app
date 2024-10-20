
import os
import sys


def resource(relative_path: str) -> str:
    '''Return absolute path of relative_path.'''

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.abspath(relative_path)
