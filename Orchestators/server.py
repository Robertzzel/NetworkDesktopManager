import signal
from Orchestators.orchestrator import Orchestrator
import zmq.asyncio, sys
import zmq.sugar
from subprocess import Popen
from pathlib import Path
from typing import *
import asyncio


class Server(Orchestrator):
    def __init__(self, image_address, input_address, sound_address):
        self._process_pool: List[Popen] = []
        self._running_tasks: asyncio.Future = None
        self._context = zmq.asyncio.Context()

        self._socket_image_client: zmq.sugar.Socket = self._context.socket(zmq.PUSH)
        self._socket_image_client.bind(f"tcp://{image_address}")

        self._socket_sound_client: zmq.sugar.Socket = self._context.socket(zmq.PUSH)
        self._socket_sound_client.bind(f"tcp://{sound_address}")

        self._socket_input_client: zmq.sugar.Socket = self._context.socket(zmq.PULL)
        self._socket_input_client.bind(f"tcp://{input_address}")

        self._socket_img_snd: zmq.sugar.Socket = self._context.socket(zmq.PULL)
        self._port_img_snd = self._socket_img_snd.bind_to_random_port(f"tcp://*")
        self._socket_img_snd.RCVTIMEO = 10000

        self._socket_input: zmq.sugar.Socket = self._context.socket(zmq.PUSH)
        self._port_input = self._socket_input.bind_to_random_port(f"tcp://*")
        self._socket_input.RCVTIMEO = 10000

    async def start(self):
        print("Starting server")

        base_path = Path(__file__).parent.parent
        process_paths = [base_path / "Producers" / "image_generator.py", base_path / "Producers" / "sound_generator.py", base_path / "Consumers" / "input_executor.py"]
        process_port = [self._port_img_snd, self._port_img_snd, self._port_input]

        for file, port in zip(process_paths, process_port):
            self._process_pool.append(Popen([sys.executable, str(file), str(port)]))

        self._running_tasks = asyncio.gather(
            self._manage_sounds_images(),
            self._manage_inputs()
        )

        try:
            await self._running_tasks
        except asyncio.CancelledError:
            pass
        await self.cancel_processes()

    async def _manage_sounds_images(self):
        while True:
            try:
                img_or_sound = await self._socket_img_snd.recv_pyobj()
            except Exception as ex:
                print(ex)
                break
            if img_or_sound[0] == 0:
                self._socket_image_client.send_pyobj(img_or_sound[1])
            elif img_or_sound[0] == 1:
                self._socket_sound_client.send_pyobj(img_or_sound[1])

    async def _manage_inputs(self):
        while True:
            try:
                action = await self._socket_input_client.recv_string()
            except Exception as ex:
                print(ex)
                break
            self._socket_input.send_string(action)

    async def cancel_tasks(self):
        if self._running_tasks is not None and not self._running_tasks.done():
            self._running_tasks.cancel()
            try:
                await self._running_tasks
            except asyncio.CancelledError:
                pass

    async def cancel_processes(self):
        for process in self._process_pool:
            if process.poll() is None:
                process.send_signal(signal.SIGINT)
                await asyncio.sleep(0.1)
                if process.poll() is None:
                    process.terminate()

        self._context.destroy(linger=0)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.add_signal_handler(signal.SIGINT, lambda: loop.create_task(server.cancel_tasks()))

    if len(sys.argv) == 4:
        server = Server(sys.argv[1], sys.argv[2], sys.argv[3])
        server_future = loop.create_task(server.start())
        loop.run_until_complete(server_future)
    else:
        print("Input error")



