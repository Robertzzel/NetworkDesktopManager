import time

from Tools.screenshot_tool import ScreenshotTool
from Commons.image_operations import ImageOperations
from multiprocessing import Queue, Process
from queue import Full
from configurations import Configurations


class ImageGenerator:
    def __init__(self, queue):
        Configurations.LOGGER.warning("SERVER: Initialising Image Generator...")
        self._queue: Queue = queue
        self._tool = ScreenshotTool()
        self._process: Process = None
        self._alive = True

    def start(self):
        Configurations.LOGGER.warning("SERVER: Starting Image Generator...")
        self._process = Process(target=self._start_sending)
        self._process.start()

    def _start_sending(self):
        while self._alive:
            try:
                self._queue.put_nowait(ImageOperations.encode(self._tool.get_screenshot()))
            except Full:
                pass

    def stop(self):
        if self._process.is_alive():
            Configurations.LOGGER.warning("SERVER: Stopping Image Generator...")
            self._alive = False
            self._process.kill()
            time.sleep(0.5)
            self._process.close()

    def is_alive(self):
        return self._process.is_alive() or self._alive
