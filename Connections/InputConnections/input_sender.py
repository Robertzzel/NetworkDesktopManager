from Tools.keyboard_tool import KeyboardTool, Key
from Tools.mouse_tool import MouseTool
from Connections.base_connection import BaseConnection
from Commons.input_actions import InputActions
from threading import Thread
from queue import Queue


class InputSender(BaseConnection):
    def __init__(self, queue: Queue):
        self._queue = queue
        self._keyboard = KeyboardTool()
        self._mouse = MouseTool()

    def start(self):
        Thread(target=self._keyboard.listen_keyboard, args=(self.on_press, self.on_release,)).start()
        Thread(target=self._mouse.listen_for_clicks, args=(self._on_move, self._on_click)).start()

    def on_press(self, key):
        if type(key) != Key:
            self._queue.put(f"{InputActions.PRESS.value}:{key.char}".encode())
            #self.send_message(self._socket, f"{InputActions.PRESS.value}:{key.char}".encode(), Configurations.INPUT_MAX_SIZE)
        else:
            self._queue.put(f"{InputActions.PRESS.value}:{key.name}".encode())
            #self.send_message(self._socket, f"{InputActions.PRESS.value}:{key.name}".encode(), Configurations.INPUT_MAX_SIZE)

    def on_release(self, key):
        if type(key) != Key:
            self._queue.put(f"{InputActions.RELEASE.value}:{key.char}".encode())
            #self.send_message(self._socket, f"{InputActions.RELEASE.value}:{key.char}".encode(), Configurations.INPUT_MAX_SIZE)
        else:
            self._queue.put(f"{InputActions.RELEASE.value}:{key.name}".encode())
            #self.send_message(self._socket, f"{InputActions.RELEASE.value}:{key.name}".encode(), Configurations.INPUT_MAX_SIZE)

    def _on_move(self, x, y):
        self._queue.put(f"{InputActions.MOVE.value}:{x},{y}".encode())
        #self.send_message(self._socket, f"{InputActions.MOVE.value}:{x},{y}".encode(), Configurations.INPUT_MAX_SIZE)

    def _on_click(self,x, y, button, pressed):
        self._queue.put(f"{InputActions.CLICK.value}:{button},{pressed}".encode())
        #self.send_message(self._socket, f"{InputActions.CLICK.value}:{button},{pressed}".encode(), Configurations.INPUT_MAX_SIZE)
