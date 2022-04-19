from cv2 import namedWindow, WINDOW_NORMAL, imshow, waitKey
from Connections.ImageConnections.image_receiver import ImageReceiver
from Connections.InputConnections.input_sender import InputSender
from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue
from threading import Thread
from Connections.base_connection import BaseConnection
from configurations import Configurations
namedWindow(Configurations.WINDOW_NAME, WINDOW_NORMAL)


class Client(BaseConnection):
    def __init__(self, address):
        self._address = address
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._connect_to_server()

        self._image_queue = Queue()
        self._input_queue = Queue()

        self._input_sender = InputSender(self._input_queue)
        self._images_receiver = ImageReceiver(self._image_queue)

        self._running = True

    def start(self):
        Thread(target=self._send_inputs).start()
        Thread(target=self._get_images).start()
        self._print_received_images()

    def _send_inputs(self):
        while self._running:
            msg: bytes = self._input_queue.get()
            self.send_message(self._socket, msg, Configurations.INPUT_MAX_SIZE)

    def _get_images(self):
        while self._running:
            img = self.receive_message(self._socket, Configurations.LENGTH_MAX_SIZE)
            self._image_queue.put(img)

    def _connect_to_server(self):
        self._socket.connect(self._address)
        print(f"Connected to {self._address}")

    def _print_received_images(self):
        for i in self._images_receiver.start_receiving():
            self.show_image(i)

    def show_image(self, image):
        imshow(Configurations.WINDOW_NAME, image)
        waitKey(1)

    def _stop(self):
        self._running = False
