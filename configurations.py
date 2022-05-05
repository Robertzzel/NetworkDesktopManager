from pathlib import Path
from Commons.computer import Computer
import logging


class Configurations:
    SERVER_IP = "localhost" #"26.146.244.0"
    IMAGES_TYPE = ".jpg"
    CURSOR_IMAGE_PATH = f"{Path(__file__).parent}/Images/cursor.png"
    LENGTH_MAX_SIZE = 8
    INPUT_MAX_SIZE = 8
    WINDOW_NAME = "LIVE"
    LOGGER_NAME = "BEST_NAME"
    LOGGER = logging.getLogger(LOGGER_NAME)
    SOUND_RECORD_SECONDS = 3
    SOUND_CHANNELS = 2
    SOUND_FRAMES = 44100
    SOUND_DEVICE = 20

