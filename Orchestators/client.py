import zmq, sys
from pathlib import Path
from Orchestators.orchestrator import Orchestrator
from configurations import Configurations
from Commons.thread_table import ThreadTable
from subprocess import Popen
from typing import *


class Client(Orchestrator):
    def __init__(self, image_address, input_address, sound_address, image_displayer_address=None):
        self._thread_pool = ThreadTable.get_threading_table()
        self._running = True
        context = zmq.Context()
        self._process_pool: List[Popen] = []
        self._image_displayer_address = image_displayer_address

        self._socket_image_server = context.socket(zmq.REQ)
        self._socket_image_server.connect(f"tcp://{image_address}")

        self._socket_sound_server = context.socket(zmq.REQ)
        self._socket_sound_server.connect(f"tcp://{sound_address}")

        self._socket_input_server = context.socket(zmq.PAIR)
        self._socket_input_server.connect(f"tcp://{input_address}")

        self._socket_image_displayer = context.socket(zmq.PAIR)
        if image_displayer_address is None:
            self._image_displayer_port = self._socket_image_displayer.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)
        else:
            self._socket_image_displayer.connect(f"tcp://{image_displayer_address}")

        self._socket_sound_player = context.socket(zmq.PAIR)
        self._sound_player_port = self._socket_sound_player.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)

        self._socket_input_generator = context.socket(zmq.PAIR)
        self._input_generator_port = self._socket_input_generator.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)

    def start(self):
        Configurations.LOGGER.warning("CLIENT: Starting...")

        base_path = Path(__file__).parent.parent
        process_paths = [base_path / "Consumers" / "sound_player.py", base_path / "Producers" / "input_generator.py"]
        process_ports = [self._sound_player_port, self._input_generator_port]

        if self._image_displayer_address is None:
            process_paths.append(base_path / "Consumers" / "image_displayer.py")
            process_ports.append(self._image_displayer_port)

        for file, port in zip(process_paths, process_ports):
            self._process_pool.append(Popen([sys.executable, str(file), str(port)]))

        self._connect()

    def _connect(self):
        self._thread_pool.new_thread(target=self._connect_to_image_server)
        # self._thread_pool.new_thread(target=self._connect_to_input_server)
        self._thread_pool.new_thread(target=self._connect_to_sound_server)

    def _connect_to_image_server(self):
        while self._running:
            self._socket_image_server.send(b"0")
            encoded_image = self._socket_image_server.recv_pyobj()
            if encoded_image == b"1":
                break
            self._socket_image_displayer.send(b"0")
            self._socket_image_displayer.send_pyobj(encoded_image)

        self._socket_image_server.send(b"1", zmq.NOBLOCK)
        self._socket_image_displayer.send(b"1", zmq.NOBLOCK)

    def _connect_to_sound_server(self):
        while self._running:
            self._socket_sound_server.send(b"0")
            sound = self._socket_sound_server.recv_pyobj()

            if sound == b"1":
                break

            self._socket_sound_player.send(b"0")
            self._socket_sound_player.send_pyobj(sound)

    def _connect_to_input_server(self):
        while self._running:
            action = self._socket_input_generator.recv_string()
            self._socket_input_server.send_string(action)

    def stop(self):
        if self._running:
            self._running = False

            self._socket_image_displayer.send(b"1")
            self._socket_sound_player.send(b"1")
            self._socket_input_generator.send(b"1")

            for process in self._process_pool:
                process.kill()

            self._thread_pool.join_all_threads(timeout=1)


if __name__ == "__main__":
    client = None
    try:
        if len(sys.argv) == 5:
            client = Client(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
            client.start()
        else:
            print("Input problem")
    except:
        if client is not None:
            print("Semnal inchdere")
            client.stop()
