import cv2 as cv
from threading import Thread
from Connections.ImageConnections.image_receiver import ImageReceiver
from Connections.MouseConnections.mouse_sender import MouseSender


class Client:
    def __init__(self, images_address, mouse_address, window_name: str):
        self._mouse_sender = MouseSender(mouse_address)
        self._images_receiver = ImageReceiver(images_address)
        self._connection = None

        self._window_name = window_name
        cv.namedWindow(self._window_name, cv.WINDOW_NORMAL)

    def start(self):
        self._images_receiver.connect()
        self._mouse_sender.connect()
        Thread(target=self._begin_sending_mouse_events).start()
        self._begin_receiving_images()

    def _begin_receiving_images(self):
        for image in self._images_receiver.start_receiving():
            self.show_image(image)

    def _begin_sending_mouse_events(self):
        self._mouse_sender.start_sending()

    def show_image(self, image):
        cv.imshow(self._window_name, image)
        cv.waitKey(1)
