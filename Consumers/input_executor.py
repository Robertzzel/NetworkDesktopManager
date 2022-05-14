from Tools.mouse_tool import MouseTool
from Tools.keyboard_tool import KeyboardTool
from Commons.input_actions import InputActions
from configurations import Configurations
import zmq, sys
import zmq.sugar


class InputExecutor:
    def __init__(self):
        self._context = zmq.Context()
        self._socket: zmq.sugar.Socket = self._context.socket(zmq.PULL)
        self._socket.connect(f"ipc://{Configurations.SERVER_EXECUTOR_FILE_LINUX}")

        self._mouse = MouseTool()
        self._keyboard = KeyboardTool()
        self.click_mapper = {
            "Button.leftTrue": self._mouse.left_press,
            "Button.leftFalse": self._mouse.left_release,
            "Button.rightTrue": self._mouse.right_press,
            "Button.rightFalse": self._mouse.right_release
        }

    def start(self):
        while True:
            data = self._socket.recv_string()
            self.execute_input(data)

    def execute_input(self, data):
        action, details = data.split(":")
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

    def clean(self):
        self._context.destroy(linger=0)


if __name__ == "__main__":
    ie = None
    try:
        ie = InputExecutor()
        ie.start()
    except Exception as ex:
        ie.clean()

