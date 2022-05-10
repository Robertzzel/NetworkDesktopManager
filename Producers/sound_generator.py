import sounddevice as sd
from queue import Queue
from threading import Thread
from configurations import Configurations
from Commons.thread_table import ThreadTable


class SoundGenerator:
    def __init__(self, queue):
        Configurations.LOGGER.warning("SERVER: Initialising Sound Generator...")
        self._queue: Queue = queue
        self._alive = True
        self._device_index = self._get_device_index()
        self._threading_table = ThreadTable.get_threading_table()
        self._thread: Thread = None

    def start(self):
        Configurations.LOGGER.warning("SERVER: Starting Sound Generator...")
        self._thread = self._threading_table.new_thread(target=self._start_recording_sending, daemon=True)
        print("sound gen")

    def _start_recording_sending(self):
        while self._alive:
            rec = sd.rec(Configurations.SOUND_RECORD_SECONDS * Configurations.SOUND_FRAMES,
                         samplerate=Configurations.SOUND_FRAMES, channels=Configurations.SOUND_CHANNELS, blocking=True)
            try:
                self._queue.put(rec.tobytes())
            except ValueError as ve:  # queue closed
                self.stop()

    def stop(self):
        Configurations.LOGGER.warning("SERVER: Stopping Sound Generator...")
        self._alive = False
        sd.stop()
        self._thread.join(0.5)

    def _get_device_index(self):
        for index, dev in enumerate(sd.query_devices()):
            if 'pulse' in dev['name']:
                return index
        raise Exception("Pulse device not found")

    def is_alive(self):
        return self._thread.is_alive()
