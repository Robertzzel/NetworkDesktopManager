import asyncio
import signal
import sys
from pathlib import Path
from UI.ui import UI
import cv2
from PIL import Image, ImageTk
import zmq.asyncio
from subprocess import Popen
from Orchestators.client import Client
from configurations import Configurations
from multiprocessing import Process


class App(UI):
    def __init__(self):
        super().__init__()
        self._window.geometry("900x900")
        self.create_widgets()
        self._socket = zmq.asyncio.Context().socket(zmq.PAIR)
        self._socket_port = self._socket.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)
        self._orchestrator_process: Popen = None

    def create_widgets(self):
        self.btn_connect = self._create_button(text="Connect", command=self.start_connecting, x_position=20, y_position=20)
        self.btn_stream = self._create_button(text="Stream", command=self.start_streaming, x_position=120, y_position=20)
        self._create_label(x_pos=220, y_pos=20, text="HOST:", font=("Arial", 18))
        entry_host, variable_host = self._create_entry(x_position=320, y_position=20, width=150, height=30)
        self._create_label(x_pos=480, y_pos=20, text="PORT:", font=("Arial", 18))
        entry_port, variable_port = self._create_entry(x_position=580, y_position=20, width=150, height=30)
        self.btn_disconnect = self._create_button(text="Disconnect", command=self.disconnect, x_position=760, y_position=20)
        self.label_image = self._create_label(x_pos=20, y_pos=80, text="No image")

    def start_streaming(self):
        server_path = str(Path(__file__).parent.parent / "Orchestators" / "server.py")
        self._orchestrator_process = Popen([sys.executable, server_path,
                                            f"{Configurations.SERVER_IP}:5101",
                                            f"{Configurations.SERVER_IP}:5102",
                                            f"{Configurations.SERVER_IP}:5103"])

    def start_connecting(self):
        client_path = str(Path(__file__).parent.parent / "Orchestators" / "client.py")
        self._orchestrator_process = Popen([sys.executable, client_path,
                                            f"{Configurations.SERVER_IP}:5101",
                                            f"{Configurations.SERVER_IP}:5102",
                                            f"{Configurations.SERVER_IP}:5103",
                                            f"{Configurations.SERVER_IP}:{self._socket_port}"])
        asyncio.run(self.update_screen())

    def disconnect(self):
        self._orchestrator_process.send_signal(signal.SIGINT)
        self._orchestrator_process.wait(timeout=3)

    async def update_screen(self):
        while True:
            action = await self._socket.recv()
            if action == b"0":
                img_tk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(await self._socket.recv_pyobj(), cv2.COLOR_BGR2RGB)))
                self.label_image.configure(image=img_tk)
                self._window.mainloop()
            elif action == b"1":
                print("gata conexiunea")
                break

if __name__ == "__main__":
    App().start()