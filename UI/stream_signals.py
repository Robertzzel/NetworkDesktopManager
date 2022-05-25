from PyQt5.QtCore import pyqtSignal, QObject


class StreamSignals(QObject):
    stream_ended_signal = pyqtSignal()
