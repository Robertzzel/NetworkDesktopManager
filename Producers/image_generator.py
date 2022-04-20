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

    def start(self):
        Configurations.LOGGER.warning("SERVER: Starting Image Generator...")
        self._process = Process(target=self._start_sending)
        self._process.start()

    def _start_sending(self):
        while True:
            encoded_image = ImageOperations.encode(self._tool.get_screenshot())
            try:
                self._queue.put_nowait(encoded_image)
            except Full:
                pass

    def stop(self):
        Configurations.LOGGER.warning("SERVER: Stopping Image Generator...")
        self._process.kill()
