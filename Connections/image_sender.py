import socket
from Screen.screenshot_tool import ScreenshotTool


class ImageSender:
    def __init__(self, address):
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tool = ScreenshotTool()
        self._stop_sending = False

    def connect(self):
        self._socket.connect(self._address)

    def _send_image_shape(self):
        screen_shape_string = self._get_image_shape_string()
        self._socket.sendall(screen_shape_string.encode())

    def _get_image_shape_string(self):
        return str(self._tool.get_screen_shape()).replace(" ", "")[1:-1]

    def start_sending(self):
        self._send_image_shape()

        while not self._stop_sending:
            self._socket.recv(4)  # send signal
            self._socket.sendall(self._tool.get_screenshot().tobytes())

    def stop(self):
        self._stop_sending = True
        self._socket.sendall(b"exit")
