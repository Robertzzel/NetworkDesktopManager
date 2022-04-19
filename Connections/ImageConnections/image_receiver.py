from Connections.base_connection import BaseConnection
from Commons.image_operations import ImageOperations
from queue import Queue
from configurations import Configurations
import cv2

cv2.namedWindow(Configurations.WINDOW_NAME, cv2.WINDOW_AUTOSIZE)

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
                self.show_image(image)
            except:
                pass

    def show_image(self, image):
        cv2.imshow(Configurations.WINDOW_NAME, image)
        cv2.waitKey(1)

    def _stop(self):
        self._running = False
