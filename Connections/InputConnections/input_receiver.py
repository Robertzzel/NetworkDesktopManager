from Commons.mouse_tool import MouseTool
from Connections.base_connection import BaseConnection
from configurations import Configurations
from Commons.keyboard_tool import KeyboardTool
from socket import socket, AF_INET, SOCK_STREAM
from Commons.input_actions import InputActions
from threading import Thread

# cursorul nu e la pozitia sageata buna

class InputReceiver(BaseConnection):
    def __init__(self, client_socket: socket):
        self._mouse = MouseTool()
        self._keyboard = KeyboardTool()
        self._client_socket = client_socket

        self.click_mapper = {
            "Button.leftTrue": self._mouse.left_press,
            "Button.leftFalse": self._mouse.left_release,
            "Button.rightTrue": self._mouse.right_press,
            "Button.rightFalse": self._mouse.right_release
        }

    def start(self):
        Thread(target=self._start_receiving).start()

    def _start_receiving(self):
        while True:
            data = self.receive_message(self._client_socket, Configurations.INPUT_MAX_SIZE).decode()
            try:
                action, details = data.split(":")
            except:
                continue
            action = InputActions(int(action))
            if action == InputActions.MOVE:
                x, y = details.split(",")
                self._mouse.move_pointer(x,y)
            elif action == InputActions.PRESS:
                self._keyboard.press_letter(details)
            elif action == InputActions.RELEASE:
                self._keyboard.release_letter(details)
            elif action == InputActions.CLICK:
                button, pressed = details.split(",")
                self.click_mapper[f"{button}{pressed}"]()
            else:
                print("action 404")
