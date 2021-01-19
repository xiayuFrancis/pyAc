from asyncio.tasks import sleep
import time
import asyncio
from queue import Queue
from threading import Thread


# 主线程是同步版本
def start_loop(loop):
    # 一个永远在后台运行的事件循环
    asyncio.set_event_loop(loop=loop)
    loop.run_forever()


def do_sleep(x, queue, msg=""):
    time.sleep(x)
    queue.put(msg)


queue = Queue()
new_loop = asyncio.new_event_loop()

t = Thread(target=start_loop, args=(new_loop,))
t.start()

print(time.ctime())

# 动态添加两个协程
# 这种方法，在主线程是同步的
new_loop.call_soon_threadsafe(do_sleep, 6, queue, "第一个")
new_loop.call_soon_threadsafe(do_sleep, 3, queue, "第二个")

while True:
    msg = queue.get()
    print("{} 协程运行完...".format(msg))
    print(time.ctime())
