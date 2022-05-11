import zmq, sys
from Tools.keyboard_tool import KeyboardTool, Key
from Commons.input_actions import InputActions
from threading import Thread
from Tools.mouse_tool import MouseTool


class InputGenerator:
    def __init__(self, port):
        self._keyboard = KeyboardTool()
        self._mouse = MouseTool()
        self._thread_keyboard: Thread = None
        self._thread_mouse: Thread = None
        self._socket = zmq.Context().socket(zmq.PAIR)
        self._socket.connect(f"tcp://localhost:{port}")

    def start(self):
        self._thread_keyboard = Thread(target=self._keyboard.listen_keyboard,
                                       args=(self.on_press, self.on_release,), daemon=True)
        self._thread_keyboard.start()

        self._thread_mouse = Thread(target=self._mouse.listen_for_clicks,
                                    args=(self._on_move, self._on_click), daemon=True)
        self._thread_mouse.start()

        while True:
            if self._socket.recv() == b"1":
                self.stop()

    def on_press(self, key):
        if type(key) != Key:
            self._socket.send_string(f"{InputActions.PRESS.value}:{key.char}")
        else:
            self._socket.send_string(f"{InputActions.PRESS.value}:{key.name}")

    def on_release(self, key):
        if type(key) != Key:
            self._socket.send_string(f"{InputActions.RELEASE.value}:{key.char}")
        else:
            self._socket.send_string(f"{InputActions.RELEASE.value}:{key.name}")

    def _on_move(self, x, y):
        self._socket.send_string(f"{InputActions.MOVE.value}:{x},{y}")

    def _on_click(self, x, y, button, pressed):
        self._socket.send_string(f"{InputActions.CLICK.value}:{button},{pressed}")

    def stop(self):
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        InputGenerator(sys.argv[1]).start()
