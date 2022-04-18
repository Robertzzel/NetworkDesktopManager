from Commons.mouse_tool import MouseTool
import socket


class MouseSender:
    def __init__(self, address):
        self._mouse_tool = MouseTool()
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self._socket.connect(self._address)

    def start_sending(self):
        self._mouse_tool.listen_for_clicks(on_move=self._on_move,
                                           on_click=self._on_click)

    def _on_move(self, x, y):
        self._socket.sendall(f"move:{x},{y}".encode())
        self._socket.recv(1)
        print(f"Moved {x}, {y}")

    def _on_click(self, x, y, button, pressed):
        self._socket.sendall(f"click:{button},{pressed}".encode())
        self._socket.recv(1)
        print(f"Clicked {x}, {y}, {button}")