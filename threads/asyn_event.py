import asyncio
import time

async def _sleep(x):
    time.sleep(2)
    return '暂停了{}秒！'.format(x)


coroutine = _sleep(2)
loop = asyncio.get_event_loop()

task = asyncio.ensure_future(coroutine)
loop.run_until_complete(task)

# task.result() 可以取得返回结果
print('返回结果：{}'.format(task.result()))


def callback(future):
    print('这里是回调函数，获取返回结果是：', future.result())

coroutine2 = _sleep(2)

task2 = asyncio.ensure_future(coroutine2)
# 添加回调函数
task2.add_done_callback(callback)
loop2 = asyncio.get_event_loop()

loop2.run_until_complete(task2)