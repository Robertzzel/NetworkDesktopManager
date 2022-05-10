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
        self._alive = True

    def start(self):
        Configurations.LOGGER.warning("CLIENT: Starting Image Displayer...")
        self._process = Process(target=self._start_receiving)
        self._process.start()

    def _start_receiving(self):
        namedWindow(Configurations.WINDOW_NAME, WINDOW_NORMAL)
        while self._alive:
            try:
                image = ImageOperations.decode(self._queue.get(timeout=1))
                self._show_image(image)
            except Exception as ex:
                pass

    def stop(self):
        Configurations.LOGGER.warning("CLIENT: Stopping Image Displayer...")
        if self._process is not None and self._process.is_alive():
            self._alive = False
            self._process.kill()
            time.sleep(0.5)
            self._process.close()
            destroyAllWindows()

    @staticmethod
    def _show_image(image):
        imshow(Configurations.WINDOW_NAME, image)
        waitKey(1)

    def is_alive(self):
        return self._process.is_alive()
