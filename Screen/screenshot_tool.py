import cv2
import pyautogui
import numpy as np


class ScreenshotTool:

    def __init__(self):
        screenshot = pyautogui.screenshot()
        self._screen_shape = np.array(screenshot).shape

    def get_screenshot(self):
        cursor_image = ScreenshotTool._get_cursor_image()
        cursor_x, cursor_y = pyautogui.position()
        screenshot_without_cursor = np.array(pyautogui.screenshot())

        try:
            screenshot_without_cursor[cursor_y: cursor_y + cursor_image.shape[0],
                                      cursor_x: cursor_x + cursor_image.shape[1]] = cursor_image
        except:
            pass

        return screenshot_without_cursor

    @staticmethod
    def _get_screenshot_without_cursor():
        screenshot_without_cursor = np.array(pyautogui.screenshot())
        return cv2.cvtColor(screenshot_without_cursor, cv2.COLOR_RGB2RGBA)

    @staticmethod
    def _get_cursor_image():
        cursor_image = cv2.imread("Images/cursor.png", cv2.IMREAD_UNCHANGED)
        cursor_new_dimensions = (cursor_image.shape[0] // 10, cursor_image.shape[1] // 10)
        cursor_image = cv2.resize(cursor_image, cursor_new_dimensions, interpolation=cv2.INTER_AREA)
        return cursor_image

    def get_screen_shape(self):
        return self._screen_shape
