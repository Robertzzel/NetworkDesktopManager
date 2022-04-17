from pathlib import Path
from Commons.computer import Computer


class Configurations:
    SERVER_IP = Computer.get_wifi_ip_address() # "26.146.244.0"
    IMAGES_TYPE = ".jpg"
    CURSOR_IMAGE_PATH = f"{Path(__file__).parent}\\Images\\cursor.jpg"
