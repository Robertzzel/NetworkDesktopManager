from pynput.mouse import Listener, Controller, Button


class MouseTool:
    def __init__(self):
        self._controller = Controller()

    @staticmethod
    def listen_for_clicks(on_move, on_click):
        with Listener(on_move=on_move, on_click=on_click) as listener:
            listener.join()

    def left_press(self):
        self._controller.press(Button.left)

    def left_release(self):
        self._controller.release(Button.left)

    def right_press(self):
        self._controller.press(Button.right)

    def right_release(self):
        self._controller.release(Button.right)

