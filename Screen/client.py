from cv2 import namedWindow, WINDOW_NORMAL, imshow, waitKey
from Connections.ImageConnections.image_receiver import ImageReceiver
from Connections.InputConnections.input_sender import InputSender
from Connections.SoundConnections.sound_sender import SoundSender


class Client:
    def __init__(self, images_address, input_address, sound_address, window_name: str):
        self._input_sender = InputSender(input_address)
        self._sound_sender = SoundSender(sound_address)
        self._images_receiver = ImageReceiver(images_address)

        self._window_name = window_name
        namedWindow(self._window_name, WINDOW_NORMAL)

    def start(self):
        self._images_receiver.connect()
        #self._input_sender.connect()
        self._sound_sender.connect()

        #self._input_sender.start()
        self._sound_sender.start()
        self._begin_receiving_images()


    def _begin_receiving_images(self):
        for image in self._images_receiver.start_receiving():
            self.show_image(image)

    def show_image(self, image):
        imshow(self._window_name, image)
        waitKey(1)
