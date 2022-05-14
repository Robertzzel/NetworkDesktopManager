import signal
from Orchestators.orchestrator import Orchestrator
from configurations import Configurations
import zmq.asyncio, sys
import zmq.sugar
from subprocess import Popen
from pathlib import Path
from typing import *
import asyncio


class Server(Orchestrator):
    def __init__(self, image_address, input_address, sound_address):
        self._process_pool: List[Popen] = []
        self._running = True
        self._context = zmq.asyncio.Context()

        self._socket_image_client: zmq.sugar.Socket = self._context.socket(zmq.PUSH)
        self._socket_image_client.bind(f"tcp://{image_address}")
        #self._socket_image_client.RCVTIMEO = 10000

        self._socket_sound_client: zmq.sugar.Socket = self._context.socket(zmq.PUSH)
        self._socket_sound_client.bind(f"tcp://{sound_address}")
        #self._socket_sound_client.RCVTIMEO = 10000

        self._socket_input_client: zmq.sugar.Socket = self._context.socket(zmq.PULL)
        self._socket_input_client.bind(f"tcp://{input_address}")
        #self._socket_input_client.RCVTIMEO = 10000

        self.create_file(Configurations.SERVER_GENERATORS_FILE_LINUX)
        self._socket_img_snd: zmq.sugar.Socket = self._context.socket(zmq.PULL)
        self._socket_img_snd.bind(f"ipc://{Configurations.SERVER_GENERATORS_FILE_LINUX}")
        self._socket_img_snd.RCVTIMEO = 10000

        self.create_file(Configurations.SERVER_EXECUTOR_FILE_LINUX)
        self._socket_input: zmq.sugar.Socket = self._context.socket(zmq.PUSH)
        self._socket_input.bind(f"ipc://{Configurations.SERVER_EXECUTOR_FILE_LINUX}")
        self._socket_input.RCVTIMEO = 10000

    async def start(self):
        Configurations.LOGGER.warning("SERVER: Starting...")

        base_path = Path(__file__).parent.parent
        process_paths = [base_path / "Producers" / "image_generator.py", base_path / "Producers" / "sound_generator.py", base_path / "Consumers" / "input_executor.py"]

        for file in process_paths:
            self._process_pool.append(Popen([sys.executable, str(file)]))

        await asyncio.gather(
            self._manage_sounds_images(),
            self._manage_inputs()
        )

    async def _manage_sounds_images(self):
        while self._running:
            img_or_sound = await self._socket_img_snd.recv_pyobj()
            if img_or_sound[0] == 0:
                self._socket_image_client.send_pyobj(img_or_sound[1])
            elif img_or_sound[0] == 1:
                self._socket_sound_client.send_pyobj(img_or_sound[1])
                print("Trimis sunet")

    async def _manage_inputs(self):
        while self._running:
            action = await self._socket_input_client.recv_string()
            self._socket_input.send(action)

    def stop(self):
        if self._running:
            Configurations.LOGGER.warning("SERVER: Stopping...")
            self._running = False
            for process in self._process_pool:
                process.send_signal(signal.SIGINT)

            self._context.destroy(linger=0)


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


