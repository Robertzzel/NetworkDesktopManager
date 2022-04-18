from Commons.mouse_tool import MouseTool
from socket import socket, AF_INET, SOCK_DGRAM
from Connections.base_connection import BaseConnection
from configurations import Configurations


class MouseReceiver(BaseConnection):
    def __init__(self, address):
        self._mouse_tool = MouseTool()
        self._address = address
        self._socket = socket(AF_INET, SOCK_DGRAM)
        self._socket.bind(address)
        # self._sender_connection: socket.socket = None

    # def connect(self):
    #     self._socket.listen()
    #     self._sender_connection, _ = self._socket.accept()

    def start_receiving(self):
        while True:
            #data = self.receive_message(self._sender_connection, Configurations.MOUSE_MAX_SIZE).decode()
            data = self._socket.recvfrom(100)[0].decode()
            action, details = data.split(":")
            if action == "click":
                button, pressed = details.split(",")
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
            elif action == "move":
                x, y = details.split(",")
                self._mouse_tool.move_pointer(int(x), int(y))
            else:
                print("action 404")



