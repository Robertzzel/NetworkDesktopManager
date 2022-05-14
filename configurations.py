from pathlib import Path
from Commons.computer import Computer
import logging


class Configurations:
    SERVER_IP = Computer.get_wifi_ip_address() #"26.146.244.0"
    IMAGES_TYPE = ".jpg"
    CURSOR_IMAGE_PATH = f"{Path(__file__).parent}/Images/cursor.png"
    LENGTH_MAX_SIZE = 16
    INPUT_MAX_SIZE = 8
    WINDOW_NAME = "LIVE"
    LOGGER_NAME = "BEST_NAME"
    LOGGER = logging.getLogger(LOGGER_NAME)
    SOUND_RECORD_SECONDS = 1
    SOUND_CHANNELS = 2
    SOUND_FRAMES = int(44100/16)
    SOUND_DEVICE = 20
    SERVER_GENERATORS_FILE_LINUX = "/tmp/alo_aici_pyzmq/0"
    SERVER_EXECUTOR_FILE_LINUX = "/tmp/alo_aici_pyzmq/1"

