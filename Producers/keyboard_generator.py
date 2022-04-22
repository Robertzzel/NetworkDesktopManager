from queue import Queue
from Tools.keyboard_tool import KeyboardTool, Key
from Commons.input_actions import InputActions
from threading import Thread


class KeyboardGenerator:
    def __init__(self, queue):
        self._queue: Queue = queue
        self._keyboard = KeyboardTool()

    def start(self):
        Thread(target=self._keyboard.listen_keyboard, args=(self.on_press, self.on_release,)).start()

    def on_press(self, key):
        if type(key) != Key:
            self._queue.put(f"{InputActions.PRESS.value}:{key.char}".encode())
        else:
            self._queue.put(f"{InputActions.PRESS.value}:{key.name}".encode())

    def on_release(self, key):
        if type(key) != Key:
            self._queue.put(f"{InputActions.RELEASE.value}:{key.char}".encode())
        else:
            self._queue.put(f"{InputActions.RELEASE.value}:{key.name}".encode())
