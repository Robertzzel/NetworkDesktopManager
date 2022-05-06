import time
from multiprocessing import Process
from queue import Queue
from Commons.image_operations import ImageOperations
from cv2 import namedWindow, WINDOW_NORMAL, imshow, waitKey, destroyAllWindows
from configurations import Configurations


class ImageDisplayer:
    def __init__(self, queue):
        self._queue: Queue = queue
        self._process: Process = None

    def start(self):
        Configurations.LOGGER.warning("CLIENT: Starting Image Displayer...")
        self._process = Process(target=self._start_receiving)
        self._process.start()

    def _start_receiving(self):
        namedWindow(Configurations.WINDOW_NAME, WINDOW_NORMAL)
        while True:
            encoded_image_string = self._queue.get()

            try:
                image = ImageOperations.decode(encoded_image_string)
                self.show_image(image)
            except:
                pass

    def stop(self):
        Configurations.LOGGER.warning("CLIENT: Stopping Image Displayer...")
        self._process.kill()
        destroyAllWindows()

    def show_image(self, image):
        imshow(Configurations.WINDOW_NAME, image)
        waitKey(1)
