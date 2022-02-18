from Commons.computer import Computer
from socket import socket
import cv2 as cv
import numpy as np
from itertools import accumulate
from operator import mul


class ScreenRecorder:
    def __init__(self, data_socket: socket, window_name: str):
        """
        Sending and receiving the screen
        :param data_socket: Socket used for sending, must be connected/bound
        :param window_name: Window name for the window
        """

        self._window_name = window_name
        self._data_socket = data_socket
        self._stop_request = False
        cv.namedWindow(self._window_name, cv.WINDOW_NORMAL)

    def start_sending(self):
        """
        Start sending the screen
        """
        screen_shot = Computer.get_screenshot()
        screen_shape_list = map(lambda number: str(number), screen_shot.shape)
        screen_shape_string = ",".join(screen_shape_list)

        self._data_socket.sendall(bytes(screen_shape_string, encoding="UTF-8"))
        while not self._stop_request:
            self._data_socket.recv(10)
            self._data_socket.sendall(Computer.get_screenshot().tobytes())

    def start_receiving(self):
        """
        Start receiving the screen
        """
        self._data_socket.listen(1)
        conn, address = self._data_socket.accept()

        received_shape_string = str(conn.recv(20), encoding="UTF-8")
        received_shape_list = list(map(lambda number: int(number), received_shape_string.split(",")))
        screen_total_size = max(accumulate(received_shape_list, mul))

        while not self._stop_request:
            conn.sendall(b"send")
            image = np.frombuffer(conn.recv(screen_total_size), dtype=np.uint8)
            image.shape = received_shape_list
            cv.imshow(self._window_name, image)
            cv.waitKey(1)

