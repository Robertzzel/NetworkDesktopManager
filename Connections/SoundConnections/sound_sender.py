import sounddevice as sd
from Connections.base_connection import BaseConnection
from socket import socket, AF_INET, SOCK_STREAM
from configurations import Configurations
from threading import Thread


class SoundSender(BaseConnection):
    def __init__(self, address):
        self._recording = None
        self._address = address
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._running = True

    def connect(self):
        print(f"Connection with {self._address}")
        self._socket.connect(self._address)

    def start(self):
        Thread(target=self._start_recording_sending).start()

    def _start_recording_sending(self):
        while self._running:
            rec = sd.rec(3 * 44100, channels=2, blocking=True)
            self.send_message(self._socket, rec, Configurations.LENGTH_MAX_SIZE)

    def stop(self):
        self._running = False
        self._socket.close()
