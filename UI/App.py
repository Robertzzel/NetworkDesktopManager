import signal, sys, tkinter, cv2, zmq.asyncio, zmq.sugar
from pathlib import Path
from UI.ui import UI
from subprocess import Popen
from configurations import Configurations
from Commons.image_operations import ImageOperations
from threading import Thread


class App(UI):
    def __init__(self):
        super().__init__()
        self._window.geometry("900x900")
        self.create_widgets()
        self._window.protocol("WM_DELETE_WINDOW", self.close)

        self._context = zmq.Context()
        self._socket: zmq.sugar.Socket = self._context.socket(zmq.PAIR)
        self._socket_port = self._socket.bind_to_random_port("tcp://*", min_port=6001, max_port=7004, max_tries=100)

        self._orchestrator_process: Popen = None
        self._running = True

    def create_widgets(self):
        self.btn_connect = self._create_button(text="Connect", command=lambda: Thread(target=self.connect).start(), x_position=20, y_position=20)
        self.btn_stream = self._create_button(text="Stream", command=lambda: Thread(target=self.stream).start(), x_position=120, y_position=20)
        self._create_label(x_pos=220, y_pos=20, text="HOST:", font=("Arial", 18))
        entry_host, self.variable_host = self._create_entry(x_position=320, y_position=20, width=150, height=30)
        self.btn_disconnect = self._create_button(text="Disconnect", command=self.disconnect, x_position=760, y_position=20)

        self.btn_disconnect["state"] = tkinter.DISABLED

    def stream(self):
        self._running = True

        server_path = str(Path(__file__).parent.parent / "Orchestators" / "server.py")
        self._orchestrator_process = Popen([sys.executable, server_path,
                                            f"{Configurations.SERVER_IP}:5101",
                                            f"{Configurations.SERVER_IP}:5102",
                                            f"{Configurations.SERVER_IP}:5103"])

        self.btn_connect["state"] = tkinter.DISABLED
        self.btn_stream["state"] = tkinter.DISABLED
        self.btn_disconnect["state"] = tkinter.NORMAL
        self.variable_host.set(Configurations.SERVER_IP)

    def connect(self):
        self._running = True

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
        self._running = False

        try:
            cv2.destroyWindow(Configurations.WINDOW_NAME)
            cv2.waitKey(1)
        except:
            pass

        self._orchestrator_process.send_signal(signal.SIGINT)

        self.btn_connect["state"] = tkinter.NORMAL
        self.btn_stream["state"] = tkinter.NORMAL
        self.btn_disconnect["state"] = tkinter.DISABLED

    def close(self):
        try:
            self.disconnect()
        except Exception as ex:
            pass
        self._context.destroy(linger=0)
        self._window.destroy()

    def update_screen(self):
        while self._running:
            cv2.imshow(Configurations.WINDOW_NAME, ImageOperations.decode(self._socket.recv_pyobj()))
            cv2.waitKey(1)


if __name__ == "__main__":
    app = None
    try:
        app = App()
        app.start()
    except KeyboardInterrupt:
        app.close()
