from cv2 import imencode, imdecode, IMREAD_COLOR
from configurations import Configurations
from numpy import frombuffer, uint8, ndarray


class ImageOperations:
    @staticmethod
    def encode(image: ndarray) -> bytes:
        return imencode(Configurations.IMAGES_TYPE, image)[1]

    @staticmethod
    def decode(encoded_image: bytes) -> ndarray:
        return imdecode(frombuffer(encoded_image, uint8), IMREAD_COLOR)
