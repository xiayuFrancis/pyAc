import asyncio
import random


async def coro(tag):
    await asyncio.sleep(random.uniform(0.5, 5))


loop = asyncio.get_event_loop()

tasks = [coro(i) for i in range(1, 11)]

# 【控制运行任务数】：运行第一个任务就返回
# FIRST_COMPLETED ：第一个任务完全返回
# FIRST_EXCEPTION：产生第一个异常返回
# ALL_COMPLETED：所有任务完成返回 （默认选项）
dones, pendings = loop.run_until_complete(asyncio.wait(
    tasks, return_when=asyncio.FIRST_COMPLETED))

print("第一次完成的任务数:, ", len(dones))

# 【控制时间】：运行一秒后，就返回
dones2, pendings2 = loop.run_until_complete(
    asyncio.wait(pendings, timeout=1))
print("第二次完成的任务数:", len(dones2))

# 【默认】：所有任务完成后返回
dones3, pendings3 = loop.run_until_complete(asyncio.wait(pendings2))

print("第三次完成的任务数:", len(dones3))

loop.close()
