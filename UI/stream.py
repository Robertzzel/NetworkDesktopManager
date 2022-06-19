from subprocess import Popen
from pathlib import Path
from configurations import Configurations
from stream_signals import StreamSignals
from PyQt5.QtCore import QRunnable
import sys, signal


class Stream(QRunnable):
    signals = StreamSignals()

    def __init__(self):
        super().__init__()
        self.process: Popen = None
        self.server_path = str(Path(__file__).parent.parent / "Orchestators" / "server" / "init")

    def run(self):
        self.process = Popen([self.server_path, f"{Configurations.CURRENT_IP}:5101",
                              f"{Configurations.CURRENT_IP}:5102", f"{Configurations.CURRENT_IP}:5103"])

    def stop(self):
        if self.process is not None:
            self.process.send_signal(signal.SIGINT)
        self.signals.stream_ended_signal.emit()
