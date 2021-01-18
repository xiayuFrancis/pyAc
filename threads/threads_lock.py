import threading


def job1():
    global n, lock
    lock.acquire()

    for i in range(10):
        n += 1
        print("job1", n)
    lock.release()


def job2():
    global n, lock
    with lock:
        for i in range(10):
            n += 1
            print("job2", n)


n = 0
lock = threading.Lock()
t1 = threading.Thread(target=job1)
t2 = threading.Thread(target=job2)

t1.start()
t2.start()
