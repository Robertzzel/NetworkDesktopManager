import time

from Producers.image_generator import ImageGenerator
from Consumers.input_executor import InputExecutor
from Producers.sound_generator import SoundGenerator
from Orchestators.orchestrator import Orchestrator
from multiprocessing import Queue
from socket import socket, AF_INET, SOCK_STREAM
from configurations import Configurations
from Commons.thread_table import ThreadTable


class Server(Orchestrator):
    def __init__(self, image_address, input_address, sound_address):
        Configurations.LOGGER.warning(f"SERVER: Initialising on thread {ThreadTable.get_current_thread_id()}...")

        self._image_socket = socket(AF_INET, SOCK_STREAM)
        self._image_socket.bind(image_address)
        self._input_socket = socket(AF_INET, SOCK_STREAM)
        self._input_socket.bind(input_address)
        self._sound_socket = socket(AF_INET, SOCK_STREAM)
        self._sound_socket.bind(sound_address)

        self._thread_table = ThreadTable.get_threading_table()

        self._image_queue = Queue(4)
        self._input_queue = Queue()
        self._sound_queue = Queue()

        self._images_sender = ImageGenerator(self._image_queue)
        # self._input_receiver = InputExecutor(self._input_queue)
        self._sound_receiver = SoundGenerator(self._sound_queue)

        self._running = True

    def start(self):
        Configurations.LOGGER.warning("SERVER: Starting...")
        self._connect()

        # self._input_receiver.start()
        self._sound_receiver.start()
        self._images_sender.start()

    def _connect(self):
        self._thread_table.new_thread(target=self._listen_for_image_connections)
        print("img conn")
        # self._thread_table.new_thread(target=self._listen_for_input_connection)
        self._thread_table.new_thread(target=self._listen_for_sound_connection)
        print("sound serv")

    def _listen_for_image_connections(self):
        Configurations.LOGGER.warning("SERVER: Listening for image connections...")
        self._image_socket.listen()

        connection, _ = self._image_socket.accept()
        Configurations.LOGGER.warning(f"SERVER: Connected to image client {_}")
        self._handle_image_connection(connection)

    def _handle_image_connection(self, connection):
        while self._running:
            try:
                self.send_message(connection, self._image_queue.get(timeout=3), Configurations.LENGTH_MAX_SIZE)
            except:
                self.stop()

    def _listen_for_input_connection(self):
        Configurations.LOGGER.warning("SERVER: Listening for input connections...")
        self._input_socket.listen()

        connection, _ = self._input_socket.accept()
        Configurations.LOGGER.warning(f"SERVER: Connected to input client {_}")
        self._handle_input_connection(connection)

    def _handle_input_connection(self, connection):
        while self._running:
            input_event = self.receive_message(connection, Configurations.INPUT_MAX_SIZE).decode()
            if input_event is not None:
                self._input_queue.put(input_event)
            else:
                self.stop()

    def _listen_for_sound_connection(self):
        Configurations.LOGGER.warning("SERVER: Listening for sound connections...")
        self._sound_socket.listen()

        connection, _ = self._sound_socket.accept()
        Configurations.LOGGER.warning(f"SERVER: Connected to sound client {_}")
        self._handle_sound_connection(connection)

    def _handle_sound_connection(self, connection):
        while self._running:
            try:
                self.send_message(connection, self._sound_queue.get(timeout=3), Configurations.INPUT_MAX_SIZE)
            except Exception as ex:
                self.stop()

    def stop(self):
        if self._running:
            Configurations.LOGGER.warning("SERVER: Stopping...")
            self._running = False

            self._sound_socket.close()
            self._image_socket.close()
            self._input_socket.close()

            self._thread_table.join_all_threads(timeout=1)
            Configurations.LOGGER.warning(f"SERVER: Used threads after stop {self._thread_table.number_of_alive_threads_in_table()}"
                                          f": {self._thread_table.alive_threads_in_table()}")

            self._images_sender.stop()
            # self._input_receiver.stop()
            self._sound_receiver.stop()
