from Orchestators.orchestrator import Orchestrator
from configurations import Configurations
import zmq.asyncio, sys
from subprocess import Popen
from pathlib import Path
from typing import *
import asyncio


class Server(Orchestrator):
    def __init__(self, image_address, input_address, sound_address):
        self._process_pool: List[Popen] = []
        self._running = True
        context = zmq.asyncio.Context()

        self._socket_image_client = context.socket(zmq.REP)
        self._socket_image_client.bind(f"tcp://{image_address}")
        self._socket_image_client.RCVTIMEO = 10000

        self._socket_sound_client = context.socket(zmq.REP)
        self._socket_sound_client.bind(f"tcp://{sound_address}")
        self._socket_sound_client.RCVTIMEO = 10000

        self._socket_input_client = context.socket(zmq.PAIR)
        self._socket_input_client.bind(f"tcp://{input_address}")
        self._socket_input_client.RCVTIMEO = 10000

        self._socket_image_generator = context.socket(zmq.REQ)
        self._image_generator_port = self._socket_image_generator.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)
        self._socket_image_generator.RCVTIMEO = 10000

        self._socket_sound_generator = context.socket(zmq.REQ)
        self._sound_generator_port = self._socket_sound_generator.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)
        self._socket_sound_generator.RCVTIMEO = 10000

        self._socket_input_executor = context.socket(zmq.PAIR)
        self._input_executor_port = self._socket_input_executor.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)
        self._socket_input_executor.RCVTIMEO = 10000

    async def start(self):
        Configurations.LOGGER.warning("SERVER: Starting...")

        base_path = Path(__file__).parent.parent
        process_paths = [base_path / "Producers" / "image_generator.py", base_path / "Producers" / "sound_generator.py", base_path / "Consumers" / "input_executor.py"]
        process_ports = [self._image_generator_port, self._sound_generator_port, self._input_executor_port]

        for file, port in zip(process_paths, process_ports):
            self._process_pool.append(Popen([sys.executable, str(file), str(port)]))

        await asyncio.gather(
            self._generate_and_send_screen(),
            # self._record_and_send_sounds(),
            # self._receive_and_execute_inputs()
        )
        print("GATA SV")

    async def _generate_and_send_screen(self):
        while self._running:
            self._socket_image_generator.send(b"0")
            img = await self.receive_object(self._socket_image_generator)

            action = await self.receive(self._socket_image_client)
            if action is None or img is None:
                break

            self._socket_image_client.send_pyobj(img)

    async def _record_and_send_sounds(self):
        while self._running:
            self._socket_sound_generator.send(b"0")
            sound = await self.receive_object(self._socket_sound_generator)

            action = await self.receive(self._socket_sound_client)
            if sound is None or action is None:
                break

            self._socket_sound_client.send_pyobj(sound)

    async def _receive_and_execute_inputs(self):
        while self._running:
            action = await self.receive_string(self._socket_input_client)
            if action is None or action == b"1":
                self._socket_input_executor.send(b"1", zmq.NOBLOCK)
                break

            self._socket_input_executor.send(b"0")
            self._socket_input_executor.send_string(action)

    def stop(self):
        if self._running:
            Configurations.LOGGER.warning("SERVER: Stopping...")
            self._running = False
            for process in self._process_pool:
                process.kill()


if __name__ == "__main__":
    server = None
    try:
        if len(sys.argv) == 4:
            server = Server(sys.argv[1], sys.argv[2], sys.argv[3])
            asyncio.run(server.start())
        else:
            print("Input error")
    except:
        print("Mesaj de intrerupere")
        server.stop()


