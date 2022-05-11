import time
import zmq, sys
from pathlib import Path
from Consumers.image_displayer import ImageDisplayer
from Producers.input_generator import InputGenerator
from Consumers.sound_player import SoundPlayer
from Orchestators.orchestrator import Orchestrator
from multiprocessing import Queue
from threading import Lock
from socket import socket, AF_INET, SOCK_STREAM
from configurations import Configurations
from Commons.thread_table import ThreadTable
from subprocess import Popen
from typing import *


class Client(Orchestrator):
    def __init__(self, image_address, input_address, sound_address):
        self._thread_pool = ThreadTable.get_threading_table()
        self._running = True
        context = zmq.Context()
        self._process_pool: List[Popen] = []

        self._socket_image_server = context.socket(zmq.PAIR)
        self._socket_image_server.bind(f"tcp://{image_address[0]}:{image_address[1]}")

        self._socket_sound_server = context.socket(zmq.PAIR)
        self._socket_sound_server.bind(f"tcp://{sound_address[0]}:{sound_address[1]}")

        self._socket_input_server = context.socket(zmq.PAIR)
        self._socket_input_server.bind(f"tcp://{input_address[0]}:{input_address[1]}")

        self._socket_image_displayer = context.socket(zmq.PAIR)
        self._image_displayer_port = self._socket_image_displayer.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)

        self._socket_sound_player = context.socket(zmq.PAIR)
        self._sound_player_port = self._socket_sound_player.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)

        self._socket_input_generator = context.socket(zmq.PAIR)
        self._input_generator_port = self._socket_input_generator.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)

    def start(self):
        Configurations.LOGGER.warning("CLIENT: Starting...")

        base_path = Path(__file__).parent.parent
        process_paths = [base_path / "Consumers" / "image_displayer.py", base_path / "Consumers" / "sound_player.py", base_path / "Producers" / "input_generator.py"]
        process_ports = [self._image_displayer_port, self._sound_player_port, self._input_generator_port]

        for file, port in zip(process_paths, process_ports):
            self._process_pool.append(Popen([sys.executable, file, port]))

        self._connect()

    def _connect(self):
        self._thread_pool.new_thread(target=self._connect_to_image_server)
        # self._thread_pool.new_thread(target=self._connect_to_input_server)
        # self._thread_pool.new_thread(target=self._connect_to_sound_server)

    def _connect_to_image_server(self):
        while self._running:
            encoded_image = self._socket_image_server.recv_pyobj()
            self._socket_image_displayer.send(b"0")
            self._socket_image_displayer.send_pyobj(encoded_image)
        self._socket_image_displayer.send(b"1")

    def _connect_to_sound_server(self):
        while self._running:
            sound = self._socket_sound_server.recv_pyobj()
            self._socket_sound_player.send(b"0")
            self._socket_sound_player.send_pyobj(sound)
        self._socket_sound_player.send(b"1")

    def _connect_to_input_server(self):
        while self._running:
            action = self._socket_input_generator.recv_string()
            self._socket_input_server.send_string(action)
        self._socket_input_generator.send(b"1")

    def stop(self):
        if self._running:
            self._running = False

            for process in self._process_pool:
                process.kill()

            self._thread_pool.join_all_threads(timeout=1)
