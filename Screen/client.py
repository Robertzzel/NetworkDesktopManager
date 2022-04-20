from cv2 import namedWindow, WINDOW_NORMAL, imshow, waitKey
from Connections.ImageConnections.image_receiver import ImageReceiver
from Connections.InputConnections.input_generator import InputGenerator
from Connections.SoundConnections.sound_player import SoundPlayer
from Connections.base_connection import BaseConnection
from multiprocessing import Queue
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from configurations import Configurations


class Client(BaseConnection):
    def __init__(self, image_address, input_address, sound_address, window_name: str):
        self._image_socket = socket(AF_INET, SOCK_STREAM)
        self._input_socket = socket(AF_INET, SOCK_STREAM)
        self._sound_socket = socket(AF_INET, SOCK_STREAM)
        self._image_address = image_address
        self._input_address = input_address
        self._sound_address = sound_address

        self._image_queue = Queue()
        self._input_queue = Queue()
        self._sound_queue = Queue()

        self._input_sender = InputGenerator(self._input_queue)
        self._sound_sender = SoundPlayer(self._sound_queue)
        self._images_receiver = ImageReceiver(self._image_queue)

        self._running = True
        self._connections = [self._image_socket, self._input_socket, self._sound_socket]
        self._window_name = window_name
        namedWindow(self._window_name, WINDOW_NORMAL)

    def start(self):
        self._connect()

        self._input_sender.start()
        #self._sound_sender.start()
        self._begin_receiving_images()

    def _connect(self):
        Thread(target=self._connect_to_image_server).start()
        Thread(target=self._connect_to_input_server).start()
        #Thread(target=self._connect_to_sound_server).start()

    def _connect_to_image_server(self):
        self._image_socket.connect(self._image_address)
        while self._running:
            encoded_image = self.receive_message(self._image_socket, Configurations.LENGTH_MAX_SIZE)
            self._image_queue.put(encoded_image)

    def _connect_to_input_server(self):
        self._input_socket.connect(self._input_address)
        while self._running:
            event = self._input_queue.get()
            self.send_message(self._input_socket, event, Configurations.INPUT_MAX_SIZE)

    def _connect_to_sound_server(self):
        self._sound_socket.connect(self._sound_address)
        while self._running:
            sound = self.receive_message(self._sound_socket, Configurations.INPUT_MAX_SIZE)
            self._sound_queue.put(sound)

    def _begin_receiving_images(self):
        for image in self._images_receiver.start_receiving():
            self.show_image(image)

    def show_image(self, image):
        imshow(self._window_name, image)
        waitKey(1)
