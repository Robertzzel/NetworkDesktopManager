from Connections.base_connection import BaseConnection
from configurations import Configurations
from Commons.keyboard_tool import KeyboardTool
from socket import socket, AF_INET, SOCK_STREAM


class KeyboadReceiver(BaseConnection):
    def __init__(self, address):
        self._address = address
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.bind(address)
        self._keyboard = KeyboardTool()
        self._sender_connection: socket = None

    def connect(self):
        print(f"Keyboard:Listening at {self._address}")
        self._socket.listen()
        self._sender_connection, _ = self._socket.accept()
        print(f"Connected to {self._sender_connection}")

    def start(self):
        while True:
            message = self.receive_message(self._sender_connection, Configurations.KEYBOARD_MAX_SIZE).decode()
            action, key = message.split(":")

            if action == "press":
                print("press" + key)
                self._keyboard.press_letter(key)
            elif action == "release":
                print("release" + key)
                self._keyboard.release_letter(key)
