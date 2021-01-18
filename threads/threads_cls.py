import time
from threading import Thread


class MyThread(Thread):
    def __init__(self, type="Python"):
        super().__init__()
        self.type = type

    def run(self):
        for i in range(2):
            print("hello", self.type)
            time.sleep(1)


if __name__ == "__main__":
    # 创建线程01，不指定参数
    thread_01 = MyThread()
    # 创建线程02，指定参数
    thread_02 = MyThread("MING")

    thread_01.start()
    thread_02.start()