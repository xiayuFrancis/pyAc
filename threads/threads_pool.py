import time
import threading
from concurrent.futures import ThreadPoolExecutor


def target():
    for i in range(5):
        print('running thread-{}:{}'.format(threading.get_ident(), i))
        time.sleep(1)


pool = ThreadPoolExecutor(5)

for i in range(10):
    pool.submit(target)
