from cv2 import namedWindow, WINDOW_NORMAL, imshow, waitKey
from Connections.ImageConnections.image_receiver import ImageReceiver
from Connections.InputConnections.input_sender import InputSender
from socket import socket, AF_INET, SOCK_STREAM


class Client:
    def __init__(self, address, window_name: str):
        self._address = address
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._connect_to_server()

        self._input_sender = InputSender(self._socket)
        self._images_receiver = ImageReceiver(self._socket)

        self._window_name = window_name
        namedWindow(self._window_name, WINDOW_NORMAL)

    def start(self):
        self._input_sender.start()
        self._begin_receiving_images()

    def _begin_receiving_images(self):
        for image in self._images_receiver.start_receiving():
            self.show_image(image)

    def show_image(self, image):
        imshow(self._window_name, image)
        waitKey(1)

    def _connect_to_server(self):
        self._socket.connect(self._address)
