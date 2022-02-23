from socket import socket
from Screen.screenshot_tool import ScreenshotTool


class ScreenRecorder:
    def __init__(self, data_socket: socket):
        self._data_socket = data_socket
        self._stop_request = False
        self._screenshot_tool = ScreenshotTool()

    def start_sending(self):
        self._send_screen_shape()

        while not self._stop_request:
            self._data_socket.recv(10)
            print("sending image")
            self._data_socket.sendall(self._screenshot_tool.get_screenshot().tobytes())

    def _send_screen_size(self):
        size = 1
        for nr in self._screenshot_tool.get_screen_shape():
            size *= nr
        self._data_socket.sendall(bytes(str(size), encoding="UTF-8"))

    def _send_screen_shape(self):
        screen_shape_string = self._get_screen_shape_string()
        self._data_socket.sendall(bytes(screen_shape_string, encoding="UTF-8"))

    def _get_screen_shape_string(self):
        screen_shape_list = map(lambda number: str(number), self._screenshot_tool.get_screen_shape())
        return ",".join(screen_shape_list)

    def stop_sending(self):
        self._stop_request = True
        self._data_socket.sendall(b"exit")
