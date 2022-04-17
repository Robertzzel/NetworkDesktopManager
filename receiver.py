from Screen.client import Client
from Commons.computer import Computer

ADDRESS = (Computer.get_wifi_ip_address(), 5001)
ADDRESS_MOUSE = (Computer.get_wifi_ip_address(), 5002)

if __name__ == "__main__":
    receiver = Client(ADDRESS, ADDRESS_MOUSE, "Live")
    receiver.start()
