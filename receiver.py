from Screen.client import Client
from configurations import Configurations

ADDRESS = (Configurations.SERVER_IP, 5001)
ADDRESS_MOUSE = (Configurations.SERVER_IP, 5002)
ADDRESS_KEYBOARD = (Configurations.SERVER_IP, 5003)

if __name__ == "__main__":
    receiver = Client(ADDRESS, ADDRESS_MOUSE, ADDRESS_KEYBOARD, "Live")
    receiver.start()
