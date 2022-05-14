import asyncio
import signal
import sys
import tkinter
from pathlib import Path
from UI.ui import UI
import cv2
from PIL import Image, ImageTk
import zmq.asyncio
from subprocess import Popen
from Orchestators.client import Client
from configurations import Configurations
from Commons.image_operations import ImageOperations
from threading import Thread


class App(UI):
    def __init__(self):
        super().__init__()
        self._window.geometry("900x900")
        self.create_widgets()
        self._socket = zmq.Context().socket(zmq.PAIR)
        self._socket_port = self._socket.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)
        self._orchestrator_process: Popen = None

    def create_widgets(self):
        self.btn_connect = self._create_button(text="Connect", command=lambda: Thread(target=self.start_connecting).start(), x_position=20, y_position=20)
        self.btn_stream = self._create_button(text="Stream", command=lambda: Thread(target=self.start_streaming).start(), x_position=120, y_position=20)
        self._create_label(x_pos=220, y_pos=20, text="HOST:", font=("Arial", 18))
        entry_host, self.variable_host = self._create_entry(x_position=320, y_position=20, width=150, height=30)
        # self._create_label(x_pos=480, y_pos=20, text="PORT:", font=("Arial", 18))
        # entry_port, variable_port = self._create_entry(x_position=580, y_position=20, width=150, height=30)
        self.btn_disconnect = self._create_button(text="Disconnect", command=self.disconnect, x_position=760, y_position=20)
        self._canvas = tkinter.Canvas(self._window, width=900, height=900)
        self._canvas.place(x=20, y=150)

        self.btn_disconnect["state"] = tkinter.DISABLED

    def start_streaming(self):
        server_path = str(Path(__file__).parent.parent / "Orchestators" / "server.py")
        self._orchestrator_process = Popen([sys.executable, server_path,
                                            f"{Configurations.SERVER_IP}:5101",
                                            f"{Configurations.SERVER_IP}:5102",
                                            f"{Configurations.SERVER_IP}:5103"])
        self.btn_connect["state"] = tkinter.DISABLED
        self.btn_stream["state"] = tkinter.DISABLED
        self.btn_disconnect["state"] = tkinter.NORMAL
        self.variable_host.set(Configurations.SERVER_IP)

    def start_connecting(self):
        connection_host = Configurations.SERVER_IP \
            if self.variable_host.get() == "" or self.variable_host.get() == "localhost" else self.variable_host.get()
        client_path = str(Path(__file__).parent.parent / "Orchestators" / "client.py")
        self._orchestrator_process = Popen([sys.executable, client_path,
                                            f"{connection_host}:5101",
                                            f"{connection_host}:5102",
                                            f"{connection_host}:5103",
                                            f"{connection_host}:{self._socket_port}"])

        self.btn_connect["state"] = tkinter.DISABLED
        self.btn_stream["state"] = tkinter.DISABLED
        self.btn_disconnect["state"] = tkinter.NORMAL

        self.update_screen()

    def disconnect(self):
        self._orchestrator_process.send_signal(signal.SIGINT)
        self._orchestrator_process.wait(timeout=3)

        self.btn_connect["state"] = tkinter.NORMAL
        self.btn_stream["state"] = tkinter.NORMAL
        self.btn_disconnect["state"] = tkinter.DISABLED

    def update_screen(self):
        while True:
            action = self._socket.recv()
            if action == b"0":
                img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(ImageOperations.decode(self._socket.recv_pyobj()), cv2.COLOR_BGR2RGB)))
                self._canvas.create_image(20, 20, anchor=tkinter.NW, image=img)
            elif action == b"1":
                self.disconnect()
                break


if __name__ == "__main__":
    app = App()
    app.start()