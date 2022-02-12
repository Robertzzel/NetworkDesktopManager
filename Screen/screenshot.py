from pyautogui import screenshot
from numpy import array


class Screenshot:
    @staticmethod
    def get():
        return array(screenshot())
