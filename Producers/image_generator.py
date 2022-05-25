import sys
from Tools.screenshot_tool import ScreenshotTool
from Commons.image_operations import ImageOperations
import zmq, zmq.sugar, signal


class ImageGenerator:
    def __init__(self, port):
        self._tool = ScreenshotTool()
        self._context = zmq.Context()
        self._socket: zmq.sugar.Socket = self._context.socket(zmq.PUSH)
        self._socket.connect(f"tcp://localhost:{port}")

    def start(self):
        while True:
            img = ImageOperations.encode(self._tool.get_screenshot())
            self._socket.send_pyobj((0, img))

    def clean(self):
        self._context.destroy(linger=0)
        sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda x, y: ig.clean())
    if len(sys.argv) == 2:
        ig = ImageGenerator(sys.argv[1])
        ig.start()
    else:
        print("No port found")

