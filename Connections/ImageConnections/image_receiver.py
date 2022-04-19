from Connections.base_connection import BaseConnection
from Commons.image_operations import ImageOperations
from queue import Queue

class ImageReceiver(BaseConnection):
    def __init__(self, queue: Queue):
        self._queue = queue
        self._running = True

    def start_receiving(self):
        while self._running:
            print("Receiving Image")
            encoded_image_string = self._queue.get()
            print(f"Received {len(encoded_image_string)}")

            if encoded_image_string == b"exit":
                self._stop()
                break

            try:
                image = ImageOperations.decode(encoded_image_string)
                yield image
            except:
                pass

    def _stop(self):
        self._running = False
