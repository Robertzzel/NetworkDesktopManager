import base64
import socket
import time

import cv2
import numpy as np
from Commons.screenshot_tool import ScreenshotTool
from configurations import Configurations


class ImageSender:
    def __init__(self, address):
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(address)
        self._sender_connection = None
        self._tool = ScreenshotTool()

    def connect(self):
        print(f"Listening at {self._address}")
        self._socket.listen()
        self._sender_connection, _ = self._socket.accept()
        print(f"Connected to {_}")

    def start_sending(self):
        while True:
            ok = 0
            encoded_image = self._encode_image(self._tool.get_screenshot())
            length_string = str(len(encoded_image)).rjust(Configurations.LENGTH_MAX_SIZE, "0")

            self._sender_connection.sendall(length_string.encode())
            self._sender_connection.sendall(encoded_image)
            time.sleep(1/30)

    def _encode_image(self, image: np.ndarray) -> bytes:
        status, encoded = cv2.imencode(Configurations.IMAGES_TYPE, image)
        data = np.array(encoded)
        string_data: bytes = base64.b64encode(data)
        return string_data

    def stop(self):
        self._sender_connection.close()
