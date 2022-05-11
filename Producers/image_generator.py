from Tools.screenshot_tool import ScreenshotTool
from Commons.image_operations import ImageOperations
import zmq
import sys


class ImageGenerator:
    def __init__(self, port):
        self._tool = ScreenshotTool()
        self._socket = zmq.Context().socket(zmq.REP)
        self._socket.connect(f"tcp://localhost:{port}")
        print(f"Conectat la {port}")

    def start(self):
        while True:
            action = self._socket.recv()
            if action == b'0':
                img = ImageOperations.encode(self._tool.get_screenshot())
                self._socket.send_pyobj(img)
            elif action == b"1":
                break
        print("Generator oprit")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        ImageGenerator(sys.argv[1]).start()

