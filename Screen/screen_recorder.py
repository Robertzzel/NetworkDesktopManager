from socket import socket
from Connections.image_sender import ImageSender
import socket


class Server:
    def __init__(self, images_address, mouse_address):
        self._mouse_address = mouse_address
        self._images_sender = ImageSender(images_address)
        self._mouse_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self._images_sender.connect()
        self.connect_with_mouse_sender()
        self._images_sender.start_sending()

    def connect_with_mouse_sender(self):
        self._mouse_socket.bind(self._mouse_address)
        self._mouse_socket.listen(1)
        conn, address = self._mouse_socket.accept()
        self._connection = conn

    def stop(self):
        self._images_sender.stop()
