from socket import socket
from Commons.screenshot_tool import ScreenshotTool
from configurations import Configurations
from Connections.base_connection import BaseConnection
from Commons.image_operations import ImageOperations


class ImageSender(BaseConnection):
    def __init__(self, client_socket: socket):
        self._client_socket = client_socket
        self._tool = ScreenshotTool()
        self._running = True

    def start_sending(self):
        while self._running:
            encoded_image = ImageOperations.encode(self._tool.get_screenshot())
            self.send_message(self._client_socket, encoded_image, Configurations.LENGTH_MAX_SIZE)

    def stop(self):
        self._running = False
