from Orchestators.orchestrator import Orchestrator
from configurations import Configurations
from Commons.thread_table import ThreadTable
import zmq, sys
from subprocess import Popen
from pathlib import Path
from typing import *


class Server(Orchestrator):
    def __init__(self, image_address, input_address, sound_address):
        self._thread_pool = ThreadTable.get_threading_table()
        self._process_pool: List[Popen] = []
        self._running = True
        context = zmq.Context()

        self._socket_image_client = context.socket(zmq.PAIR)
        self._socket_image_client.bind(f"tcp://{image_address}")

        self._socket_sound_client = context.socket(zmq.PAIR)
        self._socket_sound_client.bind(f"tcp://{sound_address}")

        self._socket_input_client = context.socket(zmq.PAIR)
        self._socket_input_client.bind(f"tcp://{input_address}")

        self._socket_image_generator = context.socket(zmq.REQ)
        self._image_generator_port = self._socket_image_generator.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)

        self._socket_sound_generator = context.socket(zmq.REQ)
        self._sound_generator_port = self._socket_sound_generator.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)

        self._socket_input_executor = context.socket(zmq.PAIR)
        self._input_executor_port = self._socket_input_executor.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)

    def start(self):
        Configurations.LOGGER.warning("SERVER: Starting...")

        base_path = Path(__file__).parent.parent
        process_paths = [base_path / "Producers" / "image_generator.py", base_path / "Producers" / "sound_generator.py", base_path / "Consumers" / "input_executor.py"]
        process_ports = [self._image_generator_port, self._sound_generator_port, self._input_executor_port]

        for file, port in zip(process_paths, process_ports):
            self._process_pool.append(Popen([sys.executable, str(file), str(port)]))

        self._connect()

    def _connect(self):
        self._thread_pool.new_thread(target=self._handle_image_connection)
        self._thread_pool.new_thread(target=self._handle_input_connection)
        self._thread_pool.new_thread(target=self._handle_sound_connection)

    def _handle_image_connection(self):
        while self._running:
            self._socket_image_generator.send(b"0")
            img = self._socket_image_generator.recv_pyobj()
            self._socket_image_client.send_pyobj(img)
        self._socket_image_generator.send(b"1")

    def _handle_sound_connection(self, ):
        while self._running:
            self._socket_sound_generator.send(b"0")
            sound = self._socket_sound_generator.recv_pyobj()
            self._socket_sound_client.send_pyobj(sound)
        self._socket_sound_generator.send(b"1")

    def _handle_input_connection(self):
        while self._running:
            action = self._socket_input_client.recv_string()
            self._socket_input_executor.send(b"0")
            self._socket_input_executor.send_string(action)
        self._socket_input_executor.send(b"1")

    def stop(self):
        if self._running:
            Configurations.LOGGER.warning("SERVER: Stopping...")
            self._running = False
            for process in self._process_pool:
                process.kill()
            self._thread_pool.join_all_threads(timeout=1)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        Server(sys.argv[1], sys.argv[2], sys.argv[3]).start()
    else:
        print("Input error")

