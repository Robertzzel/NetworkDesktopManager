import sys

from Tools.screenshot_tool import ScreenshotTool
from Commons.image_operations import ImageOperations
import zmq, zmq.sugar, signal
from configurations import Configurations


class ImageGenerator:
    def __init__(self):
        self._tool = ScreenshotTool()
        self._context = zmq.Context()
        self._socket: zmq.sugar.Socket = self._context.socket(zmq.PUSH)
        self._socket.setsockopt(zmq.CONFLATE, 1)
        self._socket.connect(f"ipc://{Configurations.SERVER_GENERATORS_FILE_LINUX}")

    def start(self):
        while True:
            img = ImageOperations.encode(self._tool.get_screenshot())
            self._socket.send_pyobj((0, img))

    def clean(self):
        self._context.destroy(linger=0)
        sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda x, y: ig.clean())
    ig = ImageGenerator()
    ig.start()

