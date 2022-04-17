import socket
import base64
import cv2
import numpy as np


class ImageReceiver:
    def __init__(self, address):
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(address)
        self._sender_connection = None

    def connect(self):
        self._socket.listen()
        self._sender_connection, _ = self._socket.accept()

    def start_receiving(self):
        while True:
            length = int(self._sender_connection.recv(6).decode())
            self._sender_connection.send(b"X")
            encoded_image_string = self._sender_connection.recv(length)

            if encoded_image_string == b"exit":
                self._stop()
                break

            yield self._decode_image_string(encoded_image_string)

    def _decode_image_string(self, image_string: str):
        decoded_image_string = base64.b64decode(image_string)
        encoded_image = np.frombuffer(decoded_image_string, np.uint8)
        return cv2.imdecode(encoded_image, 1)

    def _stop(self):
        self._sender_connection.close()
