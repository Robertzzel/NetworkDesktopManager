from cv2 import imread, cvtColor, COLOR_RGB2BGR, imshow, waitKey, IMREAD_COLOR, IMREAD_UNCHANGED, COLOR_RGB2BGRA
from pyautogui import screenshot
from pyautogui import position
from numpy import array, ndarray
from configurations import Configurations


class ScreenshotTool:
    def __init__(self):
        self._screen_shape = array(screenshot()).shape
        self.cursor_image: ndarray = imread(Configurations.CURSOR_IMAGE_PATH)

    def get_screenshot(self) -> ndarray:
        cursor_x, cursor_y = position()
        image = self.get_screenshot_image()

        if cursor_x > 0 and cursor_x + self.cursor_image.shape[1] < image.shape[1] \
                and cursor_y > 0 and cursor_y + self.cursor_image.shape[0] < image.shape[0]:

            for i in range(cursor_y, cursor_y + self.cursor_image.shape[0]):
                for j in range(cursor_x, cursor_x + self.cursor_image.shape[1]):
                    x = self.cursor_image[i - cursor_y, j - cursor_x, :]
                    if not(x[0] < 150 and x[1] < 100 and x[2] < 100):
                        image[i, j, :] = x

        return image

    def get_screenshot_image(self):
        rgb_image = screenshot()
        bgr_image: ndarray = cvtColor(array(rgb_image), COLOR_RGB2BGR)
        return bgr_image

    def get_screen_shape(self):
        return self._screen_shape


if __name__ == "__main__":
    st = ScreenshotTool()
    ss = st.get_screenshot()
    print(ss.shape)
    imshow("SS", ss)
    waitKey(0)