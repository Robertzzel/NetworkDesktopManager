from subprocess import Popen
from sys import executable
import receiver
import sender
import time


if __name__ == "__main__":

    receiver_process = Popen([executable, receiver.__file__])
    time.sleep(1)
    sender_process = Popen([executable, sender.__file__])
    time.sleep(1)
    input()


    receiver_process.kill()
    sender_process.kill()

