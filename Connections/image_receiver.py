import socket
import base64
import cv2
import numpy as np


class ImageReceiver:
    def __init__(self, address):
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._stop_sending = False

    def connect(self):
        print(f"tring to connect to {self._address}")
        self._socket.connect(self._address)
        print("connected")

    def start_receiving(self):
        while not self._stop_sending:
            self._socket.send(b"X")
            length = int(self._socket.recv(6).decode())
            self._socket.send(b"X")
            encoded_image_string = self._socket.recv(length).decode()

            if encoded_image_string == b"exit":
                self._stop()
                break

            try:
                image = self._decode_image_string(encoded_image_string)
                yield image
            except:
                pass

    def _decode_image_string(self, image_string: str):
        decoded_image_string = base64.b64decode(image_string)
        encoded_image = np.frombuffer(decoded_image_string, np.uint8)
        return cv2.imdecode(encoded_image, 1)

    def _stop(self):
        self._stop_sending = True
        self._socket.sendall(b"exit")