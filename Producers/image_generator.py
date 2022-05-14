import time

from Tools.screenshot_tool import ScreenshotTool
from Commons.image_operations import ImageOperations
import zmq
import zmq.sugar
from configurations import Configurations


class ImageGenerator:
    def __init__(self):
        self._tool = ScreenshotTool()
        self._context = zmq.Context()
        self._socket: zmq.sugar.Socket = self._context.socket(zmq.PUSH)
        self._socket.connect(f"ipc://{Configurations.SERVER_GENERATORS_FILE_LINUX}")

    def start(self):
        while True:
            img = ImageOperations.encode(self._tool.get_screenshot())
            self._socket.send_pyobj((0, img))
            time.sleep(1/60)

    def clean(self):
        self._context.destroy(linger=0)


if __name__ == "__main__":
    ig = None
    try:
        ig = ImageGenerator()
        ig.start()
    except Exception as ex:
        ig.clean()

