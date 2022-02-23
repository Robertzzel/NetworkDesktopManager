from Commons.computer import Computer
from Screen.screen_recorder import ScreenRecorder

ADDRESS = (Computer.get_wifi_ip_address(), 5001)
ADDRESS_MOUSE = (Computer.get_wifi_ip_address(), 5002)


if __name__ == "__main__":
    ScreenRecorder(ADDRESS, ADDRESS_MOUSE).start()
