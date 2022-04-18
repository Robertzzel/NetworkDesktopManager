from cv2 import imencode, imdecode, IMREAD_COLOR
from configurations import Configurations
from numpy import frombuffer, uint8, ndarray


class ImageOperations:
    @staticmethod
    def encode(image: ndarray) -> bytes:
        status, encoded = imencode(Configurations.IMAGES_TYPE, image)
        return encoded

    @staticmethod
    def decode(encoded_image: bytes) -> ndarray:
        encoded_image = frombuffer(encoded_image, uint8)
        return imdecode(encoded_image, IMREAD_COLOR)
