import sounddevice as sd
from threading import Thread
from queue import Queue
from configurations import Configurations
from numpy import frombuffer, float32
from Commons.thread_table import ThreadTable


class SoundPlayer:
    def __init__(self, queue):
        Configurations.LOGGER.warning("CLIENT: Initialising Sound Player...")
        self._alive = True
        self._queue: Queue = queue
        self._thread_table = ThreadTable.get_threading_table()
        self._thread: Thread = None

    def start(self):
        self._thread = self._thread_table.new_thread(target=self._start_recording_sending)
        Configurations.LOGGER.warning(f"CLIENT: Started Sound Player on thread {self._thread.ident}...")

    def _start_recording_sending(self):
        while self._alive:
            try:
                sounds = frombuffer(self._queue.get(timeout=1), float32)
                sounds.shape = (sounds.shape[0]//Configurations.SOUND_CHANNELS, Configurations.SOUND_CHANNELS)
                sd.play(sounds, Configurations.SOUND_FRAMES)
                sd.wait()
            except:
                continue

    def is_alive(self):
        return self._thread.is_alive()

    def stop(self):
        Configurations.LOGGER.warning("CLIENT: Stopping Sound Player...")
        self._alive = False
        sd.stop()
        self._thread.join(timeout=0.5)

