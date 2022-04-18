from cv2 import imread, cvtColor, COLOR_RGB2BGR, imshow, waitKey
from PIL.ImageGrab import grab
from pynput.mouse import Controller
from numpy import array, ndarray
from configurations import Configurations


class ScreenshotTool:
    def __init__(self):
        self._mouse = Controller()
        self._screen_shape = array(grab()).shape
        self.cursor_image = self.get_cursor_image()

    def get_screenshot(self) -> ndarray:
        cursor_x, cursor_y = self._mouse.position
        image = self.get_screenshot_image()

        try:
            image[cursor_y: cursor_y + self.cursor_image.shape[0],
                  cursor_x: cursor_x + self.cursor_image.shape[1]] = self.cursor_image
        except:
            pass

        return image

    def get_screenshot_image(self):
        rgb_image = grab()
        bgr_image = cvtColor(array(rgb_image), COLOR_RGB2BGR)
        #cv2.cvtColor(bgr_image, cv2.COLOR_BGR2BGRA)
        return bgr_image

    def get_cursor_image(self):
        cursor_image = imread(Configurations.CURSOR_IMAGE_PATH)
        #cv2.cvtColor(cursor_image, cv2.COLOR_BGR2BGRA)
        return cursor_image

    def get_screen_shape(self):
        return self._screen_shape


if __name__ == "__main__":
    st = ScreenshotTool()
    ss = st.get_screenshot()
    print(ss.shape)
    imshow("SS", ss)
    waitKey(0)