import base64
import socket
import time

import cv2
import numpy as np
from Commons.screenshot_tool import ScreenshotTool
from configurations import Configurations
from Connections.base_connection import BaseConnection


class ImageSender(BaseConnection):
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
            encoded_image = self._encode_image(self._tool.get_screenshot())
            self.send_message(self._sender_connection, encoded_image, Configurations.LENGTH_MAX_SIZE)
            time.sleep(1/30)

    def _encode_image(self, image: np.ndarray) -> bytes:
        status, encoded = cv2.imencode(Configurations.IMAGES_TYPE, image)
        data = np.array(encoded)
        string_data: bytes = base64.b64encode(data)
        return string_data

    def stop(self):
        self._sender_connection.close()
