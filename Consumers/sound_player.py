import sounddevice as sd
from threading import Thread
from queue import Queue
from configurations import Configurations


class SoundPlayer:
    def __init__(self, queue):
        Configurations.LOGGER.warning("CLIENT: Initialising Sound Player...")
        self._recording = None
        self._running = True
        self._queue: Queue = queue

    def start(self):
        Configurations.LOGGER.warning("CLIENT: Starting Sound Player...")
        Thread(target=self._start_recording_sending).start()

    def _start_recording_sending(self):
        while self._running:
            data = self._queue.get()
            sd.play(data, frames=44100, channels=2)
            sd.wait()

    def stop(self):
        Configurations.LOGGER.warning("CLIENT: Stopping Sound Player...")
        self._running = False