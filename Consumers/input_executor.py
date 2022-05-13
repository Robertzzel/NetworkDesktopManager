from Tools.mouse_tool import MouseTool
from Tools.keyboard_tool import KeyboardTool
from Commons.input_actions import InputActions
import zmq, sys


class InputExecutor:
    def __init__(self, port):
        self._socket = zmq.Context().socket(zmq.PAIR)
        self._socket.connect(f"tcp://localhost:{port}")
        self._mouse = MouseTool()
        self._keyboard = KeyboardTool()
        self.click_mapper = {
            "Button.leftTrue": self._mouse.left_press,
            "Button.leftFalse": self._mouse.left_release,
            "Button.rightTrue": self._mouse.right_press,
            "Button.rightFalse": self._mouse.right_release
        }

    def start(self):
        try:
            while True:
                action = self._socket.recv()
                if action == b"0":
                    data = self._socket.recv_string()
                    self.execute_input(data)
                elif action == b"1":
                    self._socket.close()
                    break
            print("Terminat")
        except:
            print("Terminat")

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


if __name__ == "__main__":
    if len(sys.argv) == 2:
        InputExecutor(sys.argv[1]).start()
    else:
        print("No port given")
