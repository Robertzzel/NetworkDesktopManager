from socket import socket
import cv2 as cv
import socket
from Connections.image_receiver import ImageReceiver

# TODO: Si clientul ar trebui sa poata da stop


class Client:
    def __init__(self, images_address, mouse_address, window_name: str):
        self._mouse_address = mouse_address
        self._images_receiver = ImageReceiver(images_address)
        self._mouse_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection = None

        self._window_name = window_name
        cv.namedWindow(self._window_name, cv.WINDOW_NORMAL)

    def start(self):
        self._images_receiver.connect()
        self.connect_with_mouse_receiver()

        for image in self._images_receiver.start_receiving():
            self.show_image(image)

    def connect_with_mouse_receiver(self):
        self._mouse_socket.connect(self._mouse_address)

    def show_image(self, image):
        cv.imshow(self._window_name, image)
        cv.waitKey(1)
