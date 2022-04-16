from socket import socket
from Screen.screenshot_tool import ScreenshotTool
import socket


class ScreenRecorder:
    def __init__(self, images_address, mouse_address):
        self._images_address = images_address
        self._mouse_address = mouse_address
        self._images_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._mouse_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection: socket.socket = None
        self._stop_request = False
        self._screenshot_tool = ScreenshotTool()

    def start(self):
        self.connect_with_image_receiver()
        self.connect_with_mouse_sender()
        self._start_sending()

    def connect_with_image_receiver(self):
        self._images_socket.connect(self._images_address)

    def connect_with_mouse_sender(self):
        self._mouse_socket.bind(self._mouse_address)
        self._mouse_socket.listen(1)
        conn, address = self._mouse_socket.accept()
        self._connection = conn

    def _start_sending(self):
        self._send_screen_shape()

        while not self._stop_request:
            self._images_socket.recv(4)
            self._images_socket.sendall(self._screenshot_tool.get_screenshot().tobytes())

    def _send_screen_shape(self):
        screen_shape_string = self._get_screen_shape_string()
        self._images_socket.sendall(screen_shape_string.encode())

    def _get_screen_shape_string(self):
        return str(self._screenshot_tool.get_screen_shape()).replace(" ", "")[1:-1]

    def stop(self):
        self._stop_request = True
        self._images_socket.sendall(b"exit")
        self._connection.close()
