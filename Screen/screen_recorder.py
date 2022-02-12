from Screen.screenshot import Screenshot
from socket import socket
import cv2 as cv
import numpy as np


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
        self._data_socket.sendall(bytes(str(Screenshot.get().size), encoding="UTF-8"))
        while not self._stop_request:
            self._data_socket.recv(10)
            self._data_socket.sendall(Screenshot.get().tobytes())

    def start_receiving(self):
        """
        Start receiving the screen
        """
        self._data_socket.listen(1)
        conn, address = self._data_socket.accept()

        img_size = int(conn.recv(10))
        while not self._stop_request:
            conn.sendall(b"send")
            image = np.frombuffer(conn.recv(img_size), dtype=np.uint8)
            image.shape = (1080, 1920, 3)
            cv.imshow(self._window_name, image)
            cv.waitKey(1)

