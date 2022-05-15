import asyncio
import signal

import zmq.asyncio, sys
from pathlib import Path
from Orchestators.orchestrator import Orchestrator
from configurations import Configurations
from subprocess import Popen
from typing import *


class Client(Orchestrator):
    def __init__(self, image_address, input_address, sound_address, image_displayer_address=None):
        self._active_tasks = None
        self._context = zmq.asyncio.Context()
        self._process_pool: List[Popen] = []

        self._socket_image_server = self._context.socket(zmq.PULL)
        self._socket_image_server.connect(f"tcp://{image_address}")
        self._socket_image_server.RCVTIMEO = 5000

        self._socket_sound_server = self._context.socket(zmq.PULL)
        self._socket_sound_server.connect(f"tcp://{sound_address}")
        self._socket_sound_server.RCVTIMEO = 5000

        self._socket_input_server = self._context.socket(zmq.PUSH)
        self._socket_input_server.connect(f"tcp://{input_address}")
        self._socket_input_server.RCVTIMEO = 5000

        self._socket_image_displayer = self._context.socket(zmq.PUSH)
        self._socket_image_displayer.connect(f"tcp://{image_displayer_address}")
        self._socket_image_displayer.RCVTIMEO = 5000

        self._socket_sound_player = self._context.socket(zmq.PUSH)
        self._sound_player_port = self._socket_sound_player.bind_to_random_port("tcp://*", min_port=6001, max_port=7004,
                                                                                max_tries=100)
        self._socket_sound_player.RCVTIMEO = 5000

        self._socket_input_generator = self._context.socket(zmq.PULL)
        self._input_generator_port = self._socket_input_generator.bind_to_random_port("tcp://*", min_port=6001,
                                                                                      max_port=7004, max_tries=100)

    async def start(self):
        base_path = Path(__file__).parent.parent
        process_paths = [base_path / "Consumers" / "sound_player.py", base_path / "Producers" / "input_generator.py"]
        process_ports = [self._sound_player_port, self._input_generator_port]

        for file, port in zip(process_paths, process_ports):
            self._process_pool.append(Popen([sys.executable, str(file), str(port)]))

        self._active_tasks = asyncio.gather(
            self._connect_to_image_server(),
            self._connect_to_sound_server(),
            # self._connect_to_input_server()
        )
        await self._active_tasks

    async def _connect_to_image_server(self):
        while True:
            encoded_image = await self.receive_object(self._socket_image_server)
            if encoded_image is None:
                break

            self._socket_image_displayer.send_pyobj(encoded_image)

    async def _connect_to_sound_server(self):
        while True:
            sound = await self.receive_object(self._socket_sound_server)
            if sound is None:
                break

            self._socket_sound_player.send_pyobj(sound)

    async def _connect_to_input_server(self):
        while True:
            action = await self.receive_string(self._socket_input_generator)
            if action is None:
                break

            self._socket_input_server.send_string(action)

    def stop(self):
        self._active_tasks.cancel()
        for process in self._process_pool:
            process.send_signal(signal.SIGINT)
        self._context.destroy(linger=0)
        sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda x, y: client.stop())
    if len(sys.argv) == 5:
        client = Client(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        try:
            asyncio.run(client.start())
        except asyncio.CancelledError:
            print("Corutine oprite")
    else:
        print("Input problem")
