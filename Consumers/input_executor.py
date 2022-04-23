from Tools.mouse_tool import MouseTool
from Tools.keyboard_tool import KeyboardTool
from Commons.input_actions import InputActions
from threading import Thread
from queue import Queue
from configurations import Configurations


class InputExecutor:
    def __init__(self, queue):
        Configurations.LOGGER.warning("SERVER: Initialising Input Executor...")

        self._mouse = MouseTool()
        self._keyboard = KeyboardTool()
        self._queue: Queue = queue
        self.click_mapper = {
            "Button.leftTrue": self._mouse.left_press,
            "Button.leftFalse": self._mouse.left_release,
            "Button.rightTrue": self._mouse.right_press,
            "Button.rightFalse": self._mouse.right_release
        }
        self._running = True

    def start(self):
        Configurations.LOGGER.warning("SERVER: Starting Input Executor...")
        Thread(target=self._start_receiving).start()

    def _start_receiving(self):
        while self._running:
            data = self._queue.get()
            try:
                action, details = data.split(":")
            except:
                continue
            action = InputActions(int(action))
            if action == InputActions.MOVE:
                x, y = details.split(",")
                self._mouse.move_pointer(int(x), int(y))
            elif action == InputActions.PRESS:
                self._keyboard.press_letter(details)
            elif action == InputActions.RELEASE:
                self._keyboard.release_letter(details)
            elif action == InputActions.CLICK:
                button, pressed = details.split(",")
                self.click_mapper[f"{button}{pressed}"]()
            else:
                print("action 404")

    def stop(self):
        Configurations.LOGGER.warning("SERVER: Stopping Input Executor")
        self._running = False
