from Connections.ImageConnections.image_sender import ImageSender
from Connections.MouseConnections.mouse_receiver import MouseReceiver
from threading import Thread
from Connections.KeyboardConnections.keyboard_receiver import KeyboadReceiver


class Server:
    def __init__(self, images_address, mouse_address, keyboard_address):
        self._mouse_receiver = MouseReceiver(mouse_address)
        self._images_sender = ImageSender(images_address)
        self._keyboard_receiver = KeyboadReceiver(keyboard_address)

    def start(self):
        self._images_sender.connect()
        self._keyboard_receiver.connect()
        #Thread(target=self._begin_receiving_mouse_events).start()
        Thread(target=self._keyboard_receiver.start).start()
        self._images_sender.start_sending()

    def _begin_receiving_mouse_events(self):
        self._mouse_receiver.start_receiving()

    def stop(self):
        self._images_sender.stop()
