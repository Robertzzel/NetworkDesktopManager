from Connections.ImageConnections.image_sender import ImageSender
from Connections.InputConnections.input_receiver import InputReceiver
from Connections.SoundConnections.sound_receiver import SoundReceiver


class Server:
    def __init__(self, image_address, input_address, sound_address):
        self._input_receiver = InputReceiver(input_address)
        self._images_sender = ImageSender(image_address)
        self._sound_receiver = SoundReceiver(sound_address)

    def start(self):
        self._images_sender.connect()
        #self._input_receiver.connect()
        self._sound_receiver.connect()
        #self._input_receiver.start()
        self._sound_receiver.start()
        self._images_sender.start_sending()

    def stop(self):
        self._images_sender.stop()