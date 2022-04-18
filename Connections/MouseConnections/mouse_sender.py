from Commons.mouse_tool import MouseTool
import socket
from Connections.base_connection import BaseConnection
from configurations import Configurations


class MouseSender(BaseConnection):
    def __init__(self, address):
        self._mouse_tool = MouseTool()
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # def connect(self):
    #     self._socket.connect(self._address)

    def start_sending(self):
        self._mouse_tool.listen_for_clicks(on_move=self._on_move,
                                           on_click=self._on_click)

    def _on_move(self, x, y):
        #self.send_message(self._socket, f"move:{x},{y}".encode(), Configurations.MOUSE_MAX_SIZE)
        self._socket.sendto(f"move:{x},{y}".encode(), self._address)
        print("moved", end=" ")

    def _on_click(self, x, y, button, pressed):
        #self.send_message(self._socket, f"click:{button},{pressed}".encode(), Configurations.MOUSE_MAX_SIZE)
        self._socket.sendto(f"click:{button},{pressed}".encode(), self._address)
        print(f"click {button}", end=" ")
