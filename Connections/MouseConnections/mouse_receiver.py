from Commons.mouse_tool import MouseTool
from socket import socket, AF_INET, SOCK_DGRAM
from Connections.base_connection import BaseConnection
from configurations import Configurations
from Connections.ImageConnections.image_sender import ImageSender


class MouseReceiver(BaseConnection):
    def __init__(self, address):
        self._mouse_tool = MouseTool()
        self._address = address
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.bind(address)

    def start_receiving(self):
        while True:
            data = self._socket.recvfrom(100)[0].decode()
            action, details = data.split(":")

            if action == "move":
                x, y = details.split(",")
                ImageSender.CURSOR_POSITIONS = (int(x), int(y))
                #self._mouse_tool.move_pointer(int(x), int(y))
            elif action == "click":
                button, pressed, x, y = details.split(",")
                if button == "Button.left":
                    if pressed == "True":
                        self._mouse_tool.left_press()
                    else:
                        self._mouse_tool.left_release()
                elif button == "Button.right":
                    if pressed == "True":
                        self._mouse_tool.right_press()
                    else:
                        self._mouse_tool.right_release()
                else:
                    print("click necunoscut")
            else:
                print("action 404")



