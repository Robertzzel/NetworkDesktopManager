import threading

from Producers.image_generator import ImageGenerator
from Consumers.input_executor import InputExecutor
from Producers.sound_generator import SoundGenerator
from Orchestators.orchestrator import Orchestrator
from multiprocessing import Queue
from socket import socket, AF_INET, SOCK_STREAM
from configurations import Configurations
from threading import Thread


class Server(Orchestrator):
    def __init__(self, image_address, input_address, sound_address):
        Configurations.LOGGER.warning("SERVER: Initialising...")

        self._image_socket = socket(AF_INET, SOCK_STREAM)
        self._image_socket.bind(image_address)
        self._input_socket = socket(AF_INET, SOCK_STREAM)
        self._input_socket.bind(input_address)
        self._sound_socket = socket(AF_INET, SOCK_STREAM)
        self._sound_socket.bind(sound_address)

        self._image_queue = Queue(4)
        self._input_queue = Queue()
        self._sound_queue = Queue()

        self._input_receiver = InputExecutor(self._input_queue)
        self._images_sender = ImageGenerator(self._image_queue)
        self._sound_receiver = SoundGenerator(self._sound_queue)

        self._running = True
        self._connections = [self._sound_socket, self._image_socket, self._input_socket]

    def start(self):
        Configurations.LOGGER.warning("SERVER: Starting...")
        self._connect()

        self._input_receiver.start()
        self._sound_receiver.start()
        self._images_sender.start()

    def _connect(self):
        Thread(target=self._listen_for_image_connections).start()
        Thread(target=self._listen_for_input_connection).start()
        Thread(target=self._listen_for_sound_connection).start()

    def _listen_for_image_connections(self):
        Configurations.LOGGER.warning("SERVER: Listening for image connections...")
        self._image_socket.listen()

        connection, _ = self._image_socket.accept()
        Configurations.LOGGER.warning(f"SERVER: Connected to image client {_}")
        Thread(target=self._handle_image_connection, args=(connection,)).start()

    def _handle_image_connection(self, connection):
        while self._running:
            img: bytes = self._image_queue.get()
            self.send_message(connection, img, Configurations.LENGTH_MAX_SIZE)

    def _listen_for_input_connection(self):
        Configurations.LOGGER.warning("SERVER: Listening for input connections...")
        self._input_socket.listen()

        connection, _ = self._input_socket.accept()
        Configurations.LOGGER.warning(f"SERVER: Connected to input client {_}")
        Thread(target=self._handle_input_connection, args=(connection,)).start()

    def _handle_input_connection(self, connection):
        while self._running:
            input_event = self.receive_message(connection, Configurations.INPUT_MAX_SIZE).decode()
            self._input_queue.put(input_event)

    def _listen_for_sound_connection(self):
        Configurations.LOGGER.warning("SERVER: Listening for sound connections...")
        self._sound_socket.listen()

        connection, _ = self._sound_socket.accept()
        Configurations.LOGGER.warning(f"SERVER: Connected to sound client {_}")
        Thread(target=self._handle_sound_connection, args=(connection,)).start()

    def _handle_sound_connection(self, connection):
        while self._running:
            sound_event = self._sound_queue.get()
            self.send_message(connection, sound_event, Configurations.INPUT_MAX_SIZE)

    def stop(self):
        Configurations.LOGGER.warning("SERVER: Stopping...")
        self._running = False
        map(lambda conn: conn.close(), self._connections)
        self._images_sender.stop()
        self._input_receiver.stop()
        self._sound_receiver.stop()
        self._input_receiver.stop()
        self._images_sender.stop()
        self._sound_receiver.stop()
