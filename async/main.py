import asyncio
import time


async def async_sleep(n):
    print('Before sleep')
    await asyncio.sleep(n)
    print('After sleep')


async def print_hello():
    print('Hello')


async def main():
    start = time.time()
    # this immediately starts working on this function without awaiting its completion
    task = asyncio.create_task(async_sleep(1))
    await async_sleep(2)
    await task
    await print_hello()
    print('total time:', time.time() - start)
    # it appears we are running the two sleep tasks in parallel even though no other threads or processes are used


if __name__ == '__main__':
    # this is running a single thread in a single process
    asyncio.run(main())
