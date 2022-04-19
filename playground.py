from queue import Queue
from time import time

if __name__ == "__main__":
    q = Queue()
    b = time()
    msg = (2500000 * "H").encode()
    print(type(msg))
    q.put(msg)
    x = q.get()
    print(type(x))
    e = time()
    print(f"{e-b}")