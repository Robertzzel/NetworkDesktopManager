import signal
import sys, zmq, zmq.sugar
from Tools.screenshot_tool import ScreenshotTool
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QThreadPool, QRunnable, QObject
from pathlib import Path
from subprocess import Popen
from configurations import Configurations
from numpy import ndarray
from Commons.image_operations import ImageOperations


class WorkerSignals(QObject):
    image_signal = pyqtSignal(ndarray)


class ImageGatherer(QRunnable):
    signals = WorkerSignals()

    def __init__(self):
        super().__init__()
        self.running = True
        self.context = zmq.Context()
        self.orchestrator_process: Popen = None

    def run(self):
        sock: zmq.sugar.Socket = self.context.socket(zmq.PAIR)
        ui_port = sock.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)
        self.start_client(ui_port)

        try:
            while self.running:
                image = sock.recv_pyobj()
                self.signals.image_signal.emit(image)
        except zmq.error.ContextTerminated:
            pass

    def start_client(self, ui_port):
        client_path = str(Path(__file__).parent.parent / "Orchestators" / "client.py")
        self.orchestrator_process = Popen([sys.executable, client_path,
                                            f"{Configurations.SERVER_IP}:5101",
                                            f"{Configurations.SERVER_IP}:5102",
                                            f"{Configurations.SERVER_IP}:5103",
                                            f"{Configurations.SERVER_IP}:{ui_port}"])

    def stop(self):
        self.running = False
        self.context.destroy(linger=0)
        if self.orchestrator_process is not None:
            self.orchestrator_process.send_signal(signal.SIGINT)


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.screenshot_tool = ScreenshotTool()
        self.image_gatherer = ImageGatherer()
        self._contex = zmq.Context()
        self._socket: zmq.sugar.Socket = self._contex.socket(zmq.PAIR)

        self.image_gatherer.signals.image_signal.connect(self.display_image)

        self._init_ui()

    def _init_ui(self):
        btn_connect = QPushButton("Connect")
        btn_connect.clicked.connect(self._start_image_gatherer)

        btn_stop = QPushButton("Stop")
        btn_stop.clicked.connect(self.stop_image_gatherer)

        btn_stream = QPushButton("Stream")
        btn_stream.clicked.connect(self.start_streaming)

        button_group_layout = QHBoxLayout()
        button_group_layout.addWidget(btn_stream)
        button_group_layout.addWidget(btn_connect)
        button_group_layout.addWidget(btn_stop)

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

        self.setLayout(main_layout)
        self.setGeometry(700, 700, 800, 600)

    def _start_image_gatherer(self):
        self.image_gatherer = ImageGatherer()
        pool = QThreadPool.globalInstance()
        pool.start(self.image_gatherer)

    def display_image(self, encoded_image):
        self.label_image.setPixmap(self.screenshot_tool.opencv_image_to_pixmap(ImageOperations.decode(encoded_image)))

    def stop_image_gatherer(self):
        self.image_gatherer.stop()

    def start_streaming(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = App()
    application.show()
    sys.exit(app.exec_())





