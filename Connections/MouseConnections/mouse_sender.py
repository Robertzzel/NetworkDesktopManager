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
        message = f"move:{x},{y}".encode()
        length = str(len(message)).rjust(100, "0")

        self._socket.sendall(length.encode())
        self._socket.sendall(message)
        print("moved", end=" ")

    def _on_click(self, x, y, button, pressed):
        message = f"click:{button},{pressed}".encode()
        length = str(len(message)).rjust(100, "0")

        self._socket.sendall(length.encode())
        self._socket.sendall(message)

        print(f"click {button}", end=" ")