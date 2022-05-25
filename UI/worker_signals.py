from PyQt5.QtCore import pyqtSignal, QObject
from numpy import ndarray


class WorkerSignals(QObject):
    image_signal = pyqtSignal(ndarray)
    final_signal = pyqtSignal()
