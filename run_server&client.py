from subprocess import Popen
from sys import executable
import run_client
import run_server
import time


if __name__ == "__main__":

    try:
        receiver_process = Popen([executable, run_client.__file__])
        time.sleep(1)
        sender_process = Popen([executable, run_server.__file__])
        time.sleep(1)
        input()
    except:
        pass


    receiver_process.kill()
    sender_process.kill()

