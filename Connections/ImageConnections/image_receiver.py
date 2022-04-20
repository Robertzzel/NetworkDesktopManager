from threading import Thread
from queue import Queue
from Commons.image_operations import ImageOperations


class ImageReceiver:
    def __init__(self, queue):
        self._queue: Queue = queue
        self._running = True

    def _start(self):
        Thread(target=self.start_receiving).start()

    def start_receiving(self):
        while self._running:
            encoded_image_string = self._queue.get()

            try:
                image = ImageOperations.decode(encoded_image_string)
                yield image
            except:
                pass

    def _stop(self):
        self._stop_sending = False