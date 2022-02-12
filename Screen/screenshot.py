from pyautogui import screenshot
from numpy import array


class Screenshot:
    @staticmethod
    def get():
        """
        :return: Screenshot in form of ndarray
        """
        return array(screenshot())
