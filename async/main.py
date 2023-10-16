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
    # it appears we are running the two sleep tasks in parallel even though no other threads or processes are used
    print('total time:', time.time() - start)
    # now we use gather() to run multiple tasks in parallel as an alternative way to run them all at the same time and
    # awaiting the final result of all of them
    try:
        await asyncio.gather(asyncio.wait_for(async_sleep(10), 5), async_sleep(2), print_hello())
    except asyncio.TimeoutError:
        print('Timed out waiting for sleep')
    print('total time:', time.time() - start)


if __name__ == '__main__':
    # this is running a single thread in a single process
    asyncio.run(main())
