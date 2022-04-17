import base64
import socket
import cv2
import numpy as np
from Screen.screenshot_tool import ScreenshotTool


class ImageSender:
    def __init__(self, address):
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._tool = ScreenshotTool()
        self._stop_sending = False

    def connect(self):
        self._socket.connect(self._address)

    def start_sending(self):
        while not self._stop_sending:
            encoded_image, length = self._encode_image(self._tool.get_screenshot())

            self._socket.sendall(str(length).encode())
            self._socket.recv(1)
            self._socket.sendall(encoded_image)

    def _send_image_shape(self):
        screen_shape_string = self._get_image_shape_string()
        self._socket.sendall(screen_shape_string.encode())

    def _encode_image(self, image: np.ndarray) -> (bytes, int):
        status, encoded = cv2.imencode(".jpg", image)
        data = np.array(encoded)
        string_data = base64.b64encode(data)
        return string_data, len(str(string_data))

    def _get_image_shape_string(self):
        return str(self._tool.get_screen_shape()).replace(" ", "")[1:-1]

    def stop(self):
        self._stop_sending = True
        self._socket.sendall(b"exit")
