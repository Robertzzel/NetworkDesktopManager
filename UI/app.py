import sys, zmq, zmq.sugar
from Tools.screenshot_tool import ScreenshotTool
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThreadPool
from Commons.image_operations import ImageOperations
from image_gatherer import ImageGatherer
from stream import Stream
from configurations import Configurations
from ipaddress import ip_address


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.screenshot_tool = ScreenshotTool()
        self._contex = zmq.Context()
        self._socket: zmq.sugar.Socket = self._contex.socket(zmq.PAIR)

        self.image_gatherer = ImageGatherer(self.get_address())
        self.image_gatherer.signals.image_signal.connect(self.display_image)
        self.image_gatherer.signals.final_signal.connect(self.set_ui_normal)

        self.stream = Stream()
        self.stream.signals.stream_ended_signal.connect(self.set_ui_normal)

        self._init_ui()

    def _init_ui(self):
        self.btn_connect = QPushButton("Connect")
        self.btn_connect.clicked.connect(self._start_image_gatherer)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.clicked.connect(self.stop)

        self.btn_stream = QPushButton("Stream")
        self.btn_stream.clicked.connect(self.start_streaming)

        button_group_layout = QHBoxLayout()
        button_group_layout.addWidget(self.btn_stream)
        button_group_layout.addWidget(self.btn_connect)
        button_group_layout.addWidget(self.btn_stop)

        self.label_address = QLabel("Address:")
        self.text_box = QLineEdit()

        address_layout = QHBoxLayout()
        address_layout.addWidget(self.label_address)
        address_layout.addWidget(self.text_box)

        self.label_image = QLabel()

        main_layout = QVBoxLayout()
        main_layout.addLayout(address_layout)
        main_layout.addLayout(button_group_layout)
        main_layout.addWidget(self.label_image)

        self.set_ui_normal()
        self.setLayout(main_layout)
        self.setGeometry(700, 700, 800, 600)

    def _start_image_gatherer(self):
        self.image_gatherer = ImageGatherer(self.get_address())
        pool = QThreadPool.globalInstance()
        pool.start(self.image_gatherer)
        self.set_ui_for_stream_or_connect()

    def display_image(self, encoded_image):
        self.label_image.setPixmap(self.screenshot_tool.opencv_image_to_pixmap(ImageOperations.decode(encoded_image)))

    def stop_image_gatherer(self):
        self.image_gatherer.stop()

    def start_streaming(self):
        self.stream = Stream()
        pool = QThreadPool.globalInstance()
        pool.start(self.stream)
        self.set_ui_for_stream_or_connect()

    def stop(self):
        if self.image_gatherer is not None:
            self.image_gatherer.stop()
        elif self.stream is not None:
            self.stream.stop()

    def set_ui_normal(self):
        self.btn_connect.setEnabled(True)
        self.btn_stream.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.label_image.clear()

        self.stream = None
        self.image_gatherer = None

    def set_ui_for_stream_or_connect(self):
        self.btn_connect.setEnabled(False)
        self.btn_stream.setEnabled(False)
        self.btn_stop.setEnabled(True)

    def get_address(self):
        try:
            address = self.text_box.text()
        except AttributeError:
            return Configurations.CURRENT_IP

        if address == '' or address == 'localhost':
            return Configurations.CURRENT_IP

        try:
            ip_address(address)
        except ValueError:
            return Configurations.CURRENT_IP
        else:
            return address


if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = App()
    application.show()
    sys.exit(app.exec_())
