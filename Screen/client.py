from cv2 import namedWindow, WINDOW_NORMAL, imshow, waitKey
from Connections.ImageConnections.image_displayer import ImageDisplayer
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
        self._images_receiver = ImageDisplayer(self._image_queue)

        self._running = True


    def start(self):
        self._connect()

        #self._input_sender.start()
        #self._sound_sender.start()
        self._images_receiver.start()

    def _connect(self):
        Thread(target=self._connect_to_image_server).start()
        #Thread(target=self._connect_to_input_server).start()
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

    def stop(self):
        self._running = False
        self._sound_socket.close()
        self._input_socket.close()
        self._image_socket.close()

        self._sound_sender.stop()
        self._images_receiver.stop()
