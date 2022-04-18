from Connections.ImageConnections.image_sender import ImageSender
from Connections.MouseConnections.mouse_receiver import MouseReceiver
from Connections.input_receiver import InputReceiver
from threading import Thread


class Server:
    def __init__(self, images_address, input_address):
        self._input_receiver = InputReceiver(input_address)
        self._images_sender = ImageSender(images_address)

    def start(self):
        self._images_sender.connect()
        self._input_receiver.connect()
        self._input_receiver.start()
        self._images_sender.start_sending()

    def stop(self):
        self._images_sender.stop()
