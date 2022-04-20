import sounddevice as sd
from queue import Queue
from threading import Thread
from configurations import Configurations


class SoundGenerator:
    def __init__(self, queue):
        Configurations.LOGGER.warning("SERVER: Initialising Sound Generator...")
        self._recording = None
        self._queue: Queue = queue
        self._running = True

    def start(self):
        Configurations.LOGGER.warning("SERVER: Starting Sound Generator...")
        Thread(target=self._start_recording_sending).start()

    def _start_recording_sending(self):
        while self._running:
            rec = sd.rec(3 * 44100, channels=2, blocking=True)
            self._queue.put(rec.tobytes())

    def stop(self):
        Configurations.LOGGER.warning("SERVER: Stopping Sound Generator...")
        self._running = False
