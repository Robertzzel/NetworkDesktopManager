import threading
from threading import Thread, active_count
from typing import *


class ThreadTable:
    _instance = None

    def __init__(self):
        self._threads = {}

    @staticmethod
    def get_threading_table():
        if ThreadTable._instance is None:
            ThreadTable._instance = ThreadTable()
        return ThreadTable._instance

    def new_thread(self, target, args=None, daemon: bool = False):
        new_thread = Thread(target=target, args=args if args is not None else (), daemon=daemon)
        new_thread.start()
        self._threads[new_thread.ident] = new_thread
        return new_thread

    def join_thread(self, ident: int, timeout: int):
        self._threads[ident].join(timeout=timeout)

    def join_all_threads(self, timeout: int):
        for th in self._threads.values():
            th.join(timeout=timeout)

    def alive_threads_in_table(self):
        alive_threads = filter(lambda th: th.is_alive(), self._threads.values())
        alive_idents = map(lambda th: str(th.ident), alive_threads)
        return ",".join(alive_idents) + "."

    def number_of_alive_threads_in_table(self):
        return len(list(filter(lambda th: th.is_alive(), self._threads.values())))

    def get_thread(self, identifier: int):
        return self._threads[identifier]

    @staticmethod
    def total_number_of_alive_threads():
        return active_count()

    @staticmethod
    def total_alive_threads_ids():
        active_threads = threading.enumerate()
        return ",".join(map(lambda th: str(th.ident), active_threads))

    @staticmethod
    def get_current_thread_id():
        return threading.current_thread().ident
