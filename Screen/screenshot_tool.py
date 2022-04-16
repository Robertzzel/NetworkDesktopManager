import cv2
import pyautogui
import numpy as np
from pathlib import Path


class ScreenshotTool:
    CURSOR_PATH = f"{Path(__file__).parent.parent}\\Images\\cursor.jpg"

    def __init__(self):
        self._screen_shape = np.array(pyautogui.screenshot()).shape

    def get_screenshot(self) -> np.ndarray:
        cursor_image = self.get_cursor_image()
        cursor_x, cursor_y = pyautogui.position()
        image = self.get_screenshot_image()

        try:
            image[cursor_y: cursor_y + cursor_image.shape[0],
                  cursor_x: cursor_x + cursor_image.shape[1]] = cursor_image
        except:
            pass

        return image

    def get_screenshot_image(self):
        rgb_image = pyautogui.screenshot()
        bgr_image = cv2.cvtColor(np.array(rgb_image), cv2.COLOR_RGB2BGR)
        return cv2.cvtColor(bgr_image, cv2.COLOR_BGR2BGRA)

    def get_cursor_image(self):
        cursor_image = cv2.imread(self.CURSOR_PATH)
        return cv2.cvtColor(cursor_image, cv2.COLOR_BGR2BGRA)

    def get_screen_shape(self):
        return self._screen_shape


if __name__ == "__main__":
    st = ScreenshotTool()
    ss = st.get_screenshot()
    ss2 = st.get_screenshot()
    cv2.imshow("SS", ss)
    cv2.waitKey(0)
    cv2.imshow("SS", ss2)
    cv2.waitKey(0)