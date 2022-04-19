from Connections.ImageConnections.image_sender import ImageSender
from Connections.InputConnections.input_receiver import InputReceiver


class Server:
    def __init__(self, address):
        self._input_receiver = InputReceiver(address)
        self._images_sender = ImageSender(address)

    def start(self):
        self._images_sender.connect()
        self._input_receiver.connect()
        self._input_receiver.start()
        self._images_sender.start_sending()

    def stop(self):
        self._images_sender.stop()