import sounddevice as sd
from queue import Queue
from threading import Thread


class SoundGenerator:
    def __init__(self, queue):
        self._recording = None
        self._queue: Queue = queue
        self._running = True

    def start(self):
        Thread(target=self._start_recording_sending).start()

    def _start_recording_sending(self):
        while self._running:
            rec = sd.rec(3 * 44100, channels=2, blocking=True)
            self._queue.put(rec.tobytes())

    def stop(self):
        self._running = False
