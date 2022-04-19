from socket import socket, AF_INET, SOCK_STREAM
from configurations import Configurations
from Connections.base_connection import BaseConnection
from Commons.image_operations import ImageOperations


class ImageReceiver(BaseConnection):
    def __init__(self, server_socket: socket):
        self._socket = server_socket
        self._running = True

    def start_receiving(self):
        while self._running:
            print("Receiving Image")
            encoded_image_string = self.receive_message(self._socket, Configurations.LENGTH_MAX_SIZE)
            print(f"Received {len(encoded_image_string)}")

            if encoded_image_string == b"exit":
                self._stop()
                break

            try:
                image = ImageOperations.decode(encoded_image_string)
                yield image
            except:
                pass

    def _stop(self):
        self._running = False
        self._socket.sendall(b"exit")
