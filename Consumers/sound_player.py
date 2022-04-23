import sounddevice as sd
from threading import Thread
from queue import Queue
from configurations import Configurations
from numpy import frombuffer, float32


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
            sounds = frombuffer(data, float32)
            sd.play(sounds)
            sd.wait()

    def stop(self):
        Configurations.LOGGER.warning("CLIENT: Stopping Sound Player...")
        self._running = False
