from socket import socket, AF_INET, SOCK_STREAM
from Commons.keyboard_tool import KeyboardTool
from Commons.mouse_tool import MouseTool
from configurations import Configurations
from Connections.base_connection import BaseConnection
from Commons.input_actions import InputActions
from threading import Thread


class InputSender(BaseConnection):
    def __init__(self, address):
        self._address = address
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._keyboard = KeyboardTool()
        self._mouse = MouseTool()

    def connect(self):
        print(f"KEyboard: trying to connect to {self._address}")
        self._socket.connect(self._address)
        print("Connected")

    def start(self):
        Thread(target=self._keyboard.listen_keyboard(on_press=self.on_press, on_release=self.on_release)).start()
        Thread(self._mouse.listen_for_clicks(on_move=self._on_move, on_click=self._on_click)).start()

    def on_press(self, key):
        try:
            self.send_message(self._socket, f"{InputActions.PRESS}:{key.char}".encode(), Configurations.INPUT_MAX_SIZE)
        except AttributeError:
            self.send_message(self._socket, f"{InputActions.PRESS}:{str(key)}".encode(), Configurations.INPUT_MAX_SIZE)

    def on_release(self, key):
        try:
            self.send_message(self._socket, f"{InputActions.RELEASE}:{key.char}".encode(), Configurations.INPUT_MAX_SIZE)
        except AttributeError:
            self.send_message(self._socket, f"{InputActions.RELEASE}:{str(key)}".encode(), Configurations.INPUT_MAX_SIZE)

    def _on_move(self, x, y):
        self.send_message(self._socket, f"{InputActions.MOVE}:{x},{y}".encode(), Configurations.INPUT_MAX_SIZE)

    def _on_click(self, button, pressed):
        self.send_message(self._socket, f"{InputActions.CLICK}:{button},{pressed}".encode(), Configurations.INPUT_MAX_SIZE)
