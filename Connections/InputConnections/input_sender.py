from socket import socket, AF_INET, SOCK_STREAM
from Commons.keyboard_tool import KeyboardTool, Key
from Commons.mouse_tool import MouseTool
from configurations import Configurations
from Connections.base_connection import BaseConnection
from Commons.input_actions import InputActions
from threading import Thread


class InputSender(BaseConnection):
    def __init__(self, server_socket: socket):
        self._socket = server_socket
        self._keyboard = KeyboardTool()
        self._mouse = MouseTool()

    def start(self):
        Thread(target=self._keyboard.listen_keyboard, args=(self.on_press, self.on_release,)).start()
        Thread(target=self._mouse.listen_for_clicks, args=(self._on_move, self._on_click)).start()

    def on_press(self, key):
        if type(key) != Key:
            self.send_message(self._socket, f"{InputActions.PRESS.value}:{key.char}".encode(), Configurations.INPUT_MAX_SIZE)
        else:
            self.send_message(self._socket, f"{InputActions.PRESS.value}:{key.name}".encode(), Configurations.INPUT_MAX_SIZE)

    def on_release(self, key):
        if type(key) != Key:
            self.send_message(self._socket, f"{InputActions.RELEASE.value}:{key.char}".encode(), Configurations.INPUT_MAX_SIZE)
        else:
            self.send_message(self._socket, f"{InputActions.RELEASE.value}:{key.name}".encode(), Configurations.INPUT_MAX_SIZE)

    def _on_move(self, x, y):
        self.send_message(self._socket, f"{InputActions.MOVE.value}:{x},{y}".encode(), Configurations.INPUT_MAX_SIZE)

    def _on_click(self,x, y, button, pressed):
        self.send_message(self._socket, f"{InputActions.CLICK.value}:{button},{pressed}".encode(), Configurations.INPUT_MAX_SIZE)
