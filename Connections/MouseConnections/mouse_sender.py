from Commons.mouse_tool import MouseTool
from socket import socket, AF_INET, SOCK_DGRAM
from Connections.base_connection import BaseConnection
from configurations import Configurations


class MouseSender(BaseConnection):
    def __init__(self, address):
        self._mouse_tool = MouseTool()
        self._address = address
        self._socket = socket(AF_INET, SOCK_DGRAM)

    def start_sending(self):
        self._mouse_tool.listen_for_clicks(on_move=self._on_move,
                                           on_click=self._on_click)

    def _on_move(self, x, y):
        self._socket.sendto(f"move:{x},{y}".encode(), self._address)

    def _on_click(self, x, y, button, pressed):
        self._socket.sendto(f"click:{button},{pressed}".encode(), self._address)

