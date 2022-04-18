from socket import socket, AF_INET, SOCK_STREAM
from Commons.screenshot_tool import ScreenshotTool
from configurations import Configurations
from Connections.base_connection import BaseConnection
from Commons.ImageOperations import ImageOperations


class ImageSender(BaseConnection):
    CURSOR_POSITIONS = (None, None)

    def __init__(self, address):
        self._address = address
        self._socket = socket(AF_INET, SOCK_STREAM)
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
            encoded_image = ImageOperations.encode(self._tool.get_screenshot(self.CURSOR_POSITIONS[0],
                                                                             self.CURSOR_POSITIONS[1]))
            self.send_message(self._sender_connection, encoded_image, Configurations.LENGTH_MAX_SIZE)

    def stop(self):
        self._sender_connection.close()
