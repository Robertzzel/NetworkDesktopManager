from queue import Queue
from Tools.keyboard_tool import KeyboardTool, Key
from Commons.input_actions import InputActions
from threading import Thread


class KeyboardGenerator:
    def __init__(self, queue):
        self._queue: Queue = queue
        self._keyboard = KeyboardTool()
        self._thread: Thread = None

    def start(self):
        self._thread = Thread(target=self._keyboard.listen_keyboard, args=(self.on_press, self.on_release,), daemon=True)
        self._thread.start()

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

    def stop(self):
        self._thread.join(1)

    def is_alive(self):
        return self._thread.is_alive()
