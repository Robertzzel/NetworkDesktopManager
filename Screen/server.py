from Connections.ImageConnections.image_sender import ImageSender
from Connections.InputConnections.input_receiver import InputReceiver
from socket import socket, AF_INET, SOCK_STREAM


class Server:
    def __init__(self, address):
        self._address = address
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.bind(address)
        self._client_connection: socket = self._connect()

        self._input_receiver = InputReceiver(self._client_connection)
        self._images_sender = ImageSender(self._client_connection)

    def start(self):
        self._input_receiver.start()
        self._images_sender.start_sending()

    # def stop(self):
    #     self._images_sender.stop()

    def _connect(self):
        self._socket.listen()
        client_connection, _ = self._socket.accept()
        return client_connection
