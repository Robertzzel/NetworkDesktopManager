import cv2
from cv2 import imread, cvtColor, COLOR_BGRA2BGR, COLOR_RGB2BGR
from PIL.ImageGrab import grab
from pyautogui import position
from numpy import array, ndarray
from configurations import Configurations
from mss import mss
from platform import platform


class ScreenshotTool:
    def __init__(self):
        self._screen_shape = array(grab()).shape
        self.cursor_image: ndarray = imread(Configurations.CURSOR_IMAGE_PATH)
        self._monitor = {
            "top": 0,
            "left": 0,
            "width": self._screen_shape[1],
            "height": self._screen_shape[0]
        }
        self._is_windows = platform().startswith("Windows")

    def get_screenshot(self) -> ndarray:
        cursor_x, cursor_y = position()
        image = self._get_screenshot_image()

        if cursor_x > 0 and cursor_x + self.cursor_image.shape[1] < image.shape[1] \
                and cursor_y > 0 and cursor_y + self.cursor_image.shape[0] < image.shape[0]:

            for i in range(cursor_y, cursor_y + self.cursor_image.shape[0]):
                for j in range(cursor_x, cursor_x + self.cursor_image.shape[1]):
                    x = self.cursor_image[i - cursor_y, j - cursor_x, :]
                    if not(x[0] < 150 and x[1] < 100 and x[2] < 100):
                        image[i, j, :] = x

        return cv2.resize(image, (800, 600), interpolation=cv2.INTER_AREA)

    def _get_screenshot_image(self):
        if self._is_windows:
            with mss() as sct:
                return cvtColor(array(sct.grab(self._monitor)), COLOR_BGRA2BGR)
        else:
            return cvtColor(array(grab()), COLOR_RGB2BGR)

    def get_screen_shape(self):
        return self._screen_shape


if __name__ == "__main__":
    pass