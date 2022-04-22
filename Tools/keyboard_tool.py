from pynput.keyboard import Controller, Key
from pynput.keyboard import Listener


class KeyboardTool:
    def __init__(self):
        self._controller = Controller()

    def listen_keyboard(self, on_press, on_release):
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def press_letter(self, letter: str):
        if len(letter) == 1:
            self._controller.press(letter)
        else:
            self._controller.press(Key[letter])

    def release_letter(self, letter: str):
        if len(letter) == 1:
            self._controller.release(letter)
        else:
            self._controller.release(Key[letter])
