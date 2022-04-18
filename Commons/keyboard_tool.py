from pynput.keyboard import Controller, Key
from pynput import keyboard


class KeyboardTool:
    def __init__(self):
        self._controller = Controller()

    def listen_keyboard(self, on_press, on_release):
        listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        listener.start()

    def press_letter(self, letter: str):
        try:
            self._controller.press(letter)
        except ValueError:
            self._controller.press(getattr(Key, letter.split(".")[1]))

    def release_letter(self, letter: str):
        try:
            self._controller.release(letter)
        except ValueError:
            self._controller.press(getattr(Key, letter.split(".")[1]))
