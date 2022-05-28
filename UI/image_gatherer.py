from pathlib import Path
from subprocess import Popen
from PyQt5.QtCore import QRunnable
import sys, zmq, zmq.sugar, signal
from worker_signals import WorkerSignals
from configurations import Configurations


class ImageGatherer(QRunnable):
    signals = WorkerSignals()

    def __init__(self, address):
        super().__init__()
        self.running = True
        self.context = zmq.Context()
        self.orchestrator_process: Popen = None
        self.address = address

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
        finally:
            self.signals.final_signal.emit()

    def start_client(self, ui_port):
        client_path = str(Path(__file__).parent.parent / "Orchestators" / "client.py")
        self.orchestrator_process = Popen([sys.executable, client_path,
                                            f"{self.address}:5101",
                                            f"{self.address}:5102",
                                            f"{self.address}:5103",
                                            f"{Configurations.CURRENT_IP}:{ui_port}"])

    def stop(self):
        self.running = False
        self.context.destroy(linger=0)
        if self.orchestrator_process is not None:
            self.orchestrator_process.send_signal(signal.SIGINT)