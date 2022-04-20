import sounddevice as sd
from threading import Thread
from queue import Queue


class SoundReceiver:
    def __init__(self, queue):
        self._recording = None
        self._running = True
        self._queue: Queue = queue

    def start(self):
        Thread(target=self._start_recording_sending).start()

    def _start_recording_sending(self):
        while self._running:
            data = self._queue.get()
            sd.play(data, frames=44100, channels=2)
            sd.wait()

    def stop(self):
        self._running = False
