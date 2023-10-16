import asyncio


async def async_sleep(n):
    await asyncio.sleep(n)
    return n


async def main():
    pending = set()
    for i in range(1, 11):
        pending.add(asyncio.create_task(async_sleep(i)))

    add_task = True

    while len(pending) > 0:
        done, pending = await asyncio.wait(pending, timeout=2)
        for d in done:
            print(await d)

        if add_task:
            pending.add(asyncio.create_task(async_sleep(1)))
            print("running additional task while pending tasks are being processed")
            add_task = False

if __name__ == '__main__':
    asyncio.run(main())