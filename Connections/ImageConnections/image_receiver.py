from socket import socket, AF_INET, SOCK_STREAM
from configurations import Configurations
from Connections.base_connection import BaseConnection
from Commons.image_operations import ImageOperations


class ImageReceiver(BaseConnection):
    def __init__(self, address):
        self._address = address
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._stop_sending = False

    def connect(self):
        print(f"tring to connect to {self._address}")
        self._socket.connect(self._address)
        print("connected")

    def start_receiving(self):
        while not self._stop_sending:
            encoded_image_string = self.receive_message(self._socket, Configurations.LENGTH_MAX_SIZE)

            if encoded_image_string == b"exit":
                self._stop()
                break

            try:
                image = ImageOperations.decode(encoded_image_string)
                yield image
            except:
                pass

    def _stop(self):
        self._stop_sending = True
        self._socket.sendall(b"exit")
