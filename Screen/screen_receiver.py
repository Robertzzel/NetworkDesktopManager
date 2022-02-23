from socket import socket
import cv2 as cv
import numpy as np
from itertools import accumulate
from operator import mul


class ScreenReceiver:
    def __init__(self, data_socket: socket, window_name: str):
        self._window_name = window_name
        self._data_socket = data_socket
        cv.namedWindow(self._window_name, cv.WINDOW_NORMAL)

    def start_receiving(self):
        conn = self._start_listening()
        screenshot_shape = self.receive_screenshot_shape(conn)
        screenshot_size = self.calculate_screenshot_size(screenshot_shape)

        while True:
            conn.sendall(b"send")
            message_received = conn.recv(screenshot_size)
            if message_received == b"exit":
                break
            print("image received")
            image = self.create_image(message_received, screenshot_shape)
            self.show_image(image)

    def _start_listening(self):
        self._data_socket.listen(1)
        conn, address = self._data_socket.accept()
        return conn

    @staticmethod
    def calculate_screenshot_size(screenshot_shape) -> int:
        return max(accumulate(screenshot_shape, mul))

    @staticmethod
    def receive_screenshot_shape(connection):
        received_shape_string = str(connection.recv(20), encoding="UTF-8")
        received_shape_list = tuple(map(lambda number: int(number), received_shape_string.split(",")))
        return received_shape_list

    @staticmethod
    def create_image(image_bytes, screenshot_shape):
        image = np.frombuffer(image_bytes, dtype=np.uint8)
        image.shape = screenshot_shape
        return image

    def show_image(self, image):
        cv.imshow(self._window_name, image)
        cv.waitKey(1)
