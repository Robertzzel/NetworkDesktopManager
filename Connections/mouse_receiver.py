from Commons.mouse_tool import MouseTool
import socket


class MouseReceiver:
    def __init__(self, address):
        self._mouse_tool = MouseTool()
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(address)
        self._sender_connection: socket.socket = None

    def connect(self):
        self._socket.listen()
        self._sender_connection, _ = self._socket.accept()

    def start_receiving(self):
        data = self._sender_connection.recv(1)