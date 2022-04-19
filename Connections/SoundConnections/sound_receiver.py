import sounddevice as sd
from Connections.base_connection import BaseConnection
from socket import socket, AF_INET, SOCK_STREAM
from configurations import Configurations
from threading import Thread


class SoundReceiver(BaseConnection):
    def __init__(self, address):
        self._recording = None
        self._address = address
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.bind(address)
        self._running = True
        self._client_connection = None

    def connect(self):
        print(f"Sound listening at {self._address}")
        self._socket.listen()
        self._client_connection, _ = self._socket.accept()
        print(f"Connected with {_}")

    def start(self):
        Thread(target=self._start_recording_sending).start()

    def _start_recording_sending(self):
        while self._running:
            data = self.receive_message(self._client_connection, self._recording)
            sd.play(data, frames=44100, channels=2)
            sd.wait()

    def stop(self):
        self._running = False
        self._socket.close()
