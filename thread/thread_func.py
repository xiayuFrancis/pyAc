import time
from threading import Thread


def target(name="Python"):
    for i in range(2):
        print("hello", name)
        time.sleep(1)


thread_01 = Thread(target=target)
thread_01.start()

thread_02 = Thread(target=target, args=("XIA",))
thread_02.start()