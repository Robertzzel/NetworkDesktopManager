from pathlib import Path
from Commons.computer import Computer
import logging, platform


class Configurations:
    SERVER_IP = Computer.get_wifi_ip_address() #"26.146.244.0"
    IMAGES_TYPE = ".jpg"
    CURSOR_IMAGE_PATH = f"{Path(__file__).parent / 'Images' / 'cursor.png'}"
    WINDOW_NAME = "LIVE"
    SOUND_RECORD_SECONDS = 3
    SOUND_CHANNELS = 2
    SOUND_FRAMES = int(44100/16)
    SERVER_GENERATORS_FILE_LINUX = "/tmp/alo_aici_pyzmq/0"
    SERVER_EXECUTOR_FILE_LINUX = "/tmp/alo_aici_pyzmq/1"
    OPERATING_SYSTEM = platform.system()

