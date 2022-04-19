from threading import Lock
sending_lock = Lock()
receiving_lock = Lock()


def secure_sending(func):
    def inner(*args, **kwargs):
        sending_lock.acquire()
        func(*args, **kwargs)
        sending_lock.release()
    return inner


def secure_receiving(func):
    def inner(*args, **kwargs):
        receiving_lock.acquire()
        func(*args, **kwargs)
        receiving_lock.release()
    return inner
