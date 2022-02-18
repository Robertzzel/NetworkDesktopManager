from uuid import getnode
from socket import socket, AF_INET, SOCK_DGRAM
from numpy import array
import pyautogui
import cv2


class Computer:
    @staticmethod
    def get_screenshot():
        """
        :return: Screenshot in form of ndarray
        """

        cursor_image = cv2.imread("Images/cursor.png", cv2.IMREAD_UNCHANGED)
        new_dimensions = (cursor_image.shape[0]//10, cursor_image.shape[1]//10)
        cursor_image = cv2.resize(cursor_image, new_dimensions, interpolation=cv2.INTER_AREA)
        cursor_x, cursor_y = pyautogui.position()

        screen = cv2.cvtColor(array(pyautogui.screenshot()), cv2.COLOR_RGB2RGBA)
        try:
            screen[cursor_y: cursor_y + cursor_image.shape[0], cursor_x: cursor_x + cursor_image.shape[1]] = cursor_image
        except:
            pass
        return screen

    @staticmethod
    def get_mac() -> str:
        """
        :return: The MAC address of the computer
        """
        return ':'.join(("%012X" % getnode())[i:i+2] for i in range(0, 12, 2))

    @staticmethod
    def get_wifi_ip_address() -> str:
        """
        :return: The IP address of wi-fi interface
        """
        s = socket(AF_INET, SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))  # the address does not matter
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip