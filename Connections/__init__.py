from threading import Lock
sending_lock = Lock()
receiving_lock = Lock()


def secure_sending(func):
    def inner():
        sending_lock.acquire()
        func()
        sending_lock.release()
    return inner


def secure_receiving(func):
    def inner():
        receiving_lock.acquire()
        func()
        receiving_lock.release()
    return inner
