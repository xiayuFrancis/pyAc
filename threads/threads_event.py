import time
import threading


class MyThread(threading.Thread):
    def __init__(self, name, event):
        super().__init__()
        self.name = name
        self.event = event

    def run(self):
        print(
            "Thread: {} start at {}".format(
                self.name, time.ctime(
                    time.time())))
        # 等待event.set
        self.event.wait()
        print(
            'Thread: {} finish at {}'.format(
                self.name, time.ctime(
                    time.time())))


threads = []
event = threading.Event()

[threads.append(MyThread(str(i), event)) for i in range(1, 6)]
event.clear()

[t.start() for t in threads]

print("等待5s....")
time.sleep(5)

print('Call All Threads...')
event.set()
