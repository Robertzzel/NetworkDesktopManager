import base64
import socket
import cv2
import numpy as np
from Commons.screenshot_tool import ScreenshotTool


class ImageSender:
    def __init__(self, address):
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(address)
        self._sender_connection = None
        self._tool = ScreenshotTool()

    def connect(self):
        self._socket.listen()
        self._sender_connection, _ = self._socket.accept()

    def start_sending(self):
        while True:
            encoded_image, length = self._encode_image(self._tool.get_screenshot())

            self._sender_connection.sendall(str(length).encode())
            self._sender_connection.recv(1)
            self._sender_connection.sendall(encoded_image)

    def _encode_image(self, image: np.ndarray) -> (bytes, int):
        status, encoded = cv2.imencode(".jpg", image)
        data = np.array(encoded)
        string_data = base64.b64encode(data)
        return string_data, len(str(string_data))

    def stop(self):
        self._sender_connection.close()
