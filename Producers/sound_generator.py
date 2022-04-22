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
        sd.default.device[0] = Configurations.SOUND_DEVICE
        sd.default.channels = Configurations.SOUND_CHANNELS

    def start(self):
        Configurations.LOGGER.warning("SERVER: Starting Sound Generator...")
        Thread(target=self._start_recording_sending).start()

    def _start_recording_sending(self):
        while self._running:
            rec = sd.rec(Configurations.SOUND_RECORD_SECONDS * Configurations.SOUND_FRAMES,
                         frames=Configurations.SOUND_FRAMES)
            sd.wait()
            self._queue.put(rec.tobytes())

    def stop(self):
        Configurations.LOGGER.warning("SERVER: Stopping Sound Generator...")
        self._running = False
