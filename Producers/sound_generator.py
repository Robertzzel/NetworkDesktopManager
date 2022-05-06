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
        self._device_index = self._get_device_index()

    def start(self):
        Configurations.LOGGER.warning("SERVER: Starting Sound Generator...")
        Thread(target=self._start_recording_sending).start()

    def _start_recording_sending(self):
        while self._running:
            rec =sd.rec(Configurations.SOUND_RECORD_SECONDS * Configurations.SOUND_FRAMES,
                        samplerate=Configurations.SOUND_FRAMES, channels=Configurations.SOUND_CHANNELS)
            sd.wait()
            self._queue.put(rec.tobytes())

    def stop(self):
        Configurations.LOGGER.warning("SERVER: Stopping Sound Generator...")
        self._running = False

    def _get_device_index(self):
        for index, dev in enumerate(sd.query_devices()):
            if 'pulse' in dev['name']:
                return index
        raise Exception("Pulse device not found")
