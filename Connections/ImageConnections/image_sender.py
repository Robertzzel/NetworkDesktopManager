from Tools.screenshot_tool import ScreenshotTool
from Commons.image_operations import ImageOperations
from multiprocessing import Queue, Process


class ImageSender:
    def __init__(self, queue):
        self._queue: Queue = queue
        self._tool = ScreenshotTool()
        self._process: Process = None

    def start(self):
        self._process = Process(target=self._start_sending)
        self._process.start()

    def _start_sending(self):
        while True:
            encoded_image = ImageOperations.encode(self._tool.get_screenshot())
            self._queue.put(encoded_image)

    def stop(self):
        self._process.kill()
