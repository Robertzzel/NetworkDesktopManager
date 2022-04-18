from Connections.base_connection import BaseConnection
from configurations import Configurations
from Commons.keyboard_tool import KeyboardTool
import socket


class KeyboardSender(BaseConnection):
    def __init__(self, address):
        self._address = address
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._keyboard = KeyboardTool()

    def connect(self):
        print(f"KEyboard: trying to connect to {self._address}")
        self._socket.connect(self._address)
        print("Connected")

    def start(self):
        self._keyboard.listen_keyboard(on_press=self.on_press, on_release=self.on_release)

    def on_press(self, key):
        self.send_message(self._socket, f"press:{key.char}".encode(), Configurations.KEYBOARD_MAX_SIZE)

    def on_release(self, key):
        self.send_message(self._socket, f"release:{key.char}".encode(), Configurations.KEYBOARD_MAX_SIZE)