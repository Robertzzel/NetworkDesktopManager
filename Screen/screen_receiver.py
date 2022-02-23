from socket import socket
import cv2 as cv
import numpy as np
import socket


class ScreenReceiver:
    def __init__(self, images_address, mouse_address, window_name: str):
        self._images_address = images_address
        self._mouse_address = mouse_address
        self._images_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._mouse_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection = None
        self._window_name = window_name
        cv.namedWindow(self._window_name, cv.WINDOW_NORMAL)

    def start(self):
        self.connect_with_image_sender()
        self.connect_with_mouse_receiver()
        self._start_receiving()

    def connect_with_image_sender(self):
        self._images_socket.bind(self._images_address)
        self._images_socket.listen(1)
        conn, address = self._images_socket.accept()
        self._connection = conn

    def connect_with_mouse_receiver(self):
        self._mouse_socket.connect(self._mouse_address)

    def _start_receiving(self):
        screen_shape = self.receive_screen_shape(self._connection)
        screen_size = self.calculate_screen_size(screen_shape)

        while True:
            self._connection.sendall(b"send")
            message_received = self._connection.recv(screen_size)
            if message_received == b"exit":
                break
            image = self.create_image(message_received, screen_shape)
            self.show_image(image)

    @staticmethod
    def calculate_screen_size(screen_shape) -> int:
        screen_size = 1
        for dimension in screen_shape:
            screen_size *= dimension
        return screen_size

    @staticmethod
    def receive_screen_shape(connection):
        received_shape_string = str(connection.recv(20), encoding="UTF-8")
        received_shape_list = tuple(map(lambda number: int(number), received_shape_string.split(",")))
        return received_shape_list

    @staticmethod
    def create_image(image_bytes, screen_shape):
        image = np.frombuffer(image_bytes, dtype=np.uint8)
        image.shape = screen_shape
        return image

    def show_image(self, image):
        cv.imshow(self._window_name, image)
        cv.waitKey(1)

    def stop(self):
        self._connection.close()
