import socket
import numpy as np


class ImageReceiver:
    def __init__(self, address):
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(address)
        self._sender_connection = None

    def connect(self):
        self._socket.listen(1)
        self._sender_connection, _ = self._socket.accept()

    def start_receiving(self):
        screen_shape = self.receive_image_shape()
        screen_size = self.calculate_image_size(screen_shape)

        while True:
            self._sender_connection.sendall(b"send")
            message_received = self._sender_connection.recv(screen_size)
            if message_received == b"exit":
                self._stop()
                break

            yield self.create_image(message_received, screen_shape)

    def calculate_image_size(self, screen_shape) -> int:
        screen_size = 1
        for dimension in screen_shape:
            screen_size *= dimension
        return screen_size

    def receive_image_shape(self):
        received_shape_string = self._sender_connection.recv(20).decode()
        received_shape_list = tuple(map(lambda number: int(number), received_shape_string.split(",")))
        return received_shape_list

    @staticmethod
    def create_image(image_bytes, screen_shape):
        image = np.frombuffer(image_bytes, dtype=np.uint8)
        image.shape = screen_shape
        return image

    def _stop(self):
        self._sender_connection.close()
