from Tools.screenshot_tool import ScreenshotTool
from Connections.base_connection import BaseConnection
from Commons.image_operations import ImageOperations
from queue import Queue
from threading import Thread


class ImageSender(BaseConnection):
    def __init__(self, queue: Queue):
        self._queue = queue
        self._tool = ScreenshotTool()
        self._running = True

    def start(self):
        Thread(target=self._start_generating).start()

    def _start_generating(self):
        while self._running:
            encoded_image = ImageOperations.encode(self._tool.get_screenshot())
            self._queue.put(encoded_image)

    def stop(self):
        self._running = False
