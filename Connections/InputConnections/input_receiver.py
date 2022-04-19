from Tools.mouse_tool import MouseTool
from Connections.base_connection import BaseConnection
from Tools.keyboard_tool import KeyboardTool
from Commons.input_actions import InputActions
from threading import Thread
from queue import Queue

# cursorul nu e la pozitia sageata buna

class InputReceiver(BaseConnection):
    def __init__(self, queue: Queue):
        self._mouse = MouseTool()
        self._keyboard = KeyboardTool()
        self._queue = queue

        self.click_mapper = {
            "Button.leftTrue": self._mouse.left_press,
            "Button.leftFalse": self._mouse.left_release,
            "Button.rightTrue": self._mouse.right_press,
            "Button.rightFalse": self._mouse.right_release
        }

    def start(self):
        Thread(target=self._start_receiving).start()

    def _start_receiving(self):
        while True:
            data = self._queue.get()
            try:
                action, details = data.split(":")
            except:
                continue
            action = InputActions(int(action))
            if action == InputActions.MOVE:
                x, y = details.split(",")
                self._mouse.move_pointer(x,y)
            elif action == InputActions.PRESS:
                self._keyboard.press_letter(details)
            elif action == InputActions.RELEASE:
                self._keyboard.release_letter(details)
            elif action == InputActions.CLICK:
                button, pressed = details.split(",")
                self.click_mapper[f"{button}{pressed}"]()
            else:
                print("action 404")
