import time
from Consumers.image_displayer import ImageDisplayer
from Producers.mouse_generator import MouseGenerator
from Producers.keyboard_generator import KeyboardGenerator
from Consumers.sound_player import SoundPlayer
from Orchestators.orchestrator import Orchestrator
from multiprocessing import Queue
from threading import Lock
from socket import socket, AF_INET, SOCK_STREAM
from configurations import Configurations
from Commons.thread_table import ThreadTable


class Client(Orchestrator):
    def __init__(self, image_address, input_address, sound_address):
        Configurations.LOGGER.warning(f"CLIENT: Initialising on thread {ThreadTable.get_current_thread_id()}...")
        self._image_socket = socket(AF_INET, SOCK_STREAM)
        self._input_socket = socket(AF_INET, SOCK_STREAM)
        self._sound_socket = socket(AF_INET, SOCK_STREAM)
        self._image_address = image_address
        self._input_address = input_address
        self._sound_address = sound_address

        self._thread_table = ThreadTable.get_threading_table()

        self._image_queue = Queue(4)
        self._keyboard_queue = Queue()
        self._mouse_queue = Queue(4)
        self._sound_queue = Queue()
        self._input_lock = Lock()

        # self._keyboard_generator = KeyboardGenerator(self._keyboard_queue)
        # self._mouse_sender = MouseGenerator(self._mouse_queue)
        self._sound_sender = SoundPlayer(self._sound_queue)
        self._images_receiver = ImageDisplayer(self._image_queue)

        self._running = True

    def start(self):
        self._connect()

        # self._mouse_sender.start()
        # self._keyboard_generator.start()
        self._sound_sender.start()
        self._images_receiver.start()

    def _connect(self):
        self._thread_table.new_thread(target=self._connect_to_image_server)
        print("for image client")
        # self._thread_table.new_thread(target=self._connect_to_input_server)
        self._thread_table.new_thread(target=self._connect_to_sound_server)
        print("sound client")

    def _connect_to_image_server(self):
        Configurations.LOGGER.warning("CLIENT: Connecting to image server...")
        self.connect_to_address(self._image_socket, self._image_address)
        Configurations.LOGGER.warning(f"CLIENT: Connected to image server at {self._image_address}")

        while self._running:
            encoded_image = self.receive_message(self._image_socket, Configurations.LENGTH_MAX_SIZE)
            if encoded_image is not None:
                self._image_queue.put(encoded_image)
            else:
                self.stop()

    def _connect_to_input_server(self):
        Configurations.LOGGER.warning("CLIENT: Connecting to input server...")
        self.connect_to_address(self._input_socket, self._input_address)
        Configurations.LOGGER.warning(f"CLIENT: Connected to input server at {self._input_address}")

        self._thread_table.new_thread(target=self._handle_keyboard_events)
        self._handle_mouse_events()

    def _handle_keyboard_events(self):
        while self._running:
            event = self._keyboard_queue.get(timeout=3)
            self._input_lock.acquire()
            try:
                self.send_message(self._input_socket, event, Configurations.INPUT_MAX_SIZE)
            except:
                self.stop()
            self._input_lock.release()

    def _handle_mouse_events(self):
        while self._running:
            event = self._mouse_queue.get(timeout=3)
            self._input_lock.acquire()
            try:
                self.send_message(self._input_socket, event, Configurations.INPUT_MAX_SIZE)
            except:
                self.stop()
            self._input_lock.release()

    def _connect_to_sound_server(self):
        Configurations.LOGGER.warning("CLIENT: Connecting to sound server...")
        self.connect_to_address(self._sound_socket, self._sound_address)
        Configurations.LOGGER.warning(f"CLIENT: Connected to sound server at {self._sound_address}")

        while self._running:
            sound = self.receive_message(self._sound_socket, Configurations.INPUT_MAX_SIZE)
            if sound is not None:
                self._sound_queue.put(sound)
            else:
                self.stop()

    def disconnect(self):
        self._sound_socket.close()
        self._input_socket.close()
        self._image_socket.close()

    def stop(self):
        if self._running:
            Configurations.LOGGER.warning("CLIENT: Stopping...")
            self._running = False
            self.disconnect()

            self._thread_table.join_all_threads(timeout=1)

            self._sound_sender.stop()
            self._images_receiver.stop()
            time.sleep(1)
            Configurations.LOGGER.warning(f"CLIENT: Used threads after stop: {self._thread_table.number_of_alive_threads_in_table()} -> "
                                          f"{self._thread_table.ac()}")

    def connect_to_address(self, sock, address):
        while self._running:
            try:
                sock.connect(address)
                break
            except:
                time.sleep(1)
