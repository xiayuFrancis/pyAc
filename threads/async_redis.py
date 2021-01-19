import time
import redis
import asyncio
from queue import Queue
from threading import Thread


def start_loop(loop):
    # 一个在后台永远运行的事件循环
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def do_sleep(x, queue: Queue):
    await asyncio.sleep(x)
    queue.put("ok")


def get_redis():
    connection_pool = redis.ConnectionPool(host='127.0.0.1', db=0)
    return redis.Redis(connection_pool=connection_pool)


def consumer():
    while True:
        task = rcon.rpop("queue")
        if not task:
            time.sleep(1)
            continue
        asyncio.run_coroutine_threadsafe(do_sleep(int(task), queue), new_loop)


if __name__ == "__main__":
    print(time.ctime())
    new_loop = asyncio.new_event_loop()

    loop_thread = Thread(target=start_loop, args=(new_loop,))
    loop_thread.setDaemon(True)
    loop_thread.start()

    rcon = get_redis()
    queue = Queue()

    consumer_thread = Thread(target=consumer)
    consumer_thread.setDaemon(True)
    consumer_thread.start()

    while True:
        msg = queue.get()
        print("协程运行完..")
        print("当前时间：", time.ctime())
