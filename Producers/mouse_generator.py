from queue import Queue
from Tools.mouse_tool import MouseTool
from Commons.input_actions import InputActions
from threading import Thread
from configurations import Configurations


class MouseGenerator:
    def __init__(self, queue):
        self._queue: Queue = queue
        self._mouse = MouseTool()
        self._thread: Thread = None

    def start(self):
        Configurations.LOGGER.warning("SERVER: Starting Input Generator...")
        self._thread = Thread(target=self._mouse.listen_for_clicks, args=(self._on_move, self._on_click), daemon=True)
        self._thread.start()

    def _on_move(self, x, y):
        self._queue.put(f"{InputActions.MOVE.value}:{x},{y}".encode())

    def _on_click(self,x, y, button, pressed):
        self._queue.put(f"{InputActions.CLICK.value}:{button},{pressed}".encode())

    def stop(self):
        self._thread.join(timeout=1)

    def is_alive(self):
        return self._thread.is_alive()
