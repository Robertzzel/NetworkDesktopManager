from threading import Thread
from Connections.ImageConnections.image_sender import ImageSender
from Connections.InputConnections.input_receiver import InputReceiver
from socket import socket, AF_INET, SOCK_STREAM
from queue import Queue
from Connections.base_connection import BaseConnection
from configurations import Configurations


class Server(BaseConnection):
    def __init__(self, address):
        self._running = True

        self._address = address
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._client_connection: socket = self._connect()

        self._input_queue = Queue()
        self._image_queue = Queue()

        self._input_receiver = InputReceiver(self._input_queue)
        self._image_generator = ImageSender(self._image_queue)

    def start(self):
        self._input_receiver.start()
        self._image_generator.start()
        Thread(target=self._capture_inputs).start()
        Thread(target=self._send_images()).start()

    def _capture_inputs(self):
        while self._running:
            msg = self.receive_message(self._client_connection,
                                       Configurations.INPUT_MAX_SIZE).decode()
            self._input_queue.put(msg)

    def _send_images(self):
        while self._running:
            image: bytes = self._image_queue.get()
            print("sent")
            self.send_message(self._client_connection, image,
                              Configurations.LENGTH_MAX_SIZE)

    # def stop(self):
    #     self._images_sender.stop()

    def _connect(self):
        self._socket.bind(self._address)
        print(f"Listenigng to {self._address}")
        self._socket.listen()
        client_connection, _ = self._socket.accept()
        print(f"connected to {_}")
        return client_connection
