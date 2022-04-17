import cv2
import pyautogui
import numpy as np
from configurations import Configurations


class ScreenshotTool:
    def __init__(self):
        self._screen_shape = np.array(pyautogui.screenshot()).shape
        self.cursor_image = self.get_cursor_image()

    def get_screenshot(self) -> np.ndarray:
        cursor_x, cursor_y = pyautogui.position()
        image = self.get_screenshot_image()

        try:
            image[cursor_y: cursor_y + self.cursor_image.shape[0],
                  cursor_x: cursor_x + self.cursor_image.shape[1]] = self.cursor_image
        except:
            pass

        return image

    def get_screenshot_image(self):
        rgb_image = pyautogui.screenshot()
        bgr_image = cv2.cvtColor(np.array(rgb_image), cv2.COLOR_RGB2BGR)
        #cv2.cvtColor(bgr_image, cv2.COLOR_BGR2BGRA)
        return bgr_image

    def get_cursor_image(self):
        cursor_image = cv2.imread(Configurations.CURSOR_IMAGE_PATH)
        #cv2.cvtColor(cursor_image, cv2.COLOR_BGR2BGRA)
        return cursor_image

    def get_screen_shape(self):
        return self._screen_shape


if __name__ == "__main__":
    st = ScreenshotTool()
    ss = st.get_screenshot()
    print(ss.shape)
    cv2.imshow("SS", ss)
    cv2.waitKey(0)