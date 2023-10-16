import asyncio
import time
import requests
import aiohttp


async def get_url_response(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_sync_url_response(url):
    return requests.get(url).text


async def main():
    urls = [
        'https://www.google.com',
        'https://wiki.python.org/moin/PythonAsyncio',
        'https://python.org',
        'https://pypi.org/project/requests',
        'https://stackoverflow.com/questions/49005651/asyncio-requests-in-python',
        'https://www.python.org/dev/peps/pep-0492',
    ]

    start = time.time()
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(get_sync_url_response(url)))

    await asyncio.gather(*tasks)

    end_time = time.time()
    print('Sync requests time taken:', end_time - start)

    start = time.time()
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(get_url_response(url)))

    await asyncio.gather(*tasks)

    end_time = time.time()
    print('Async requests time taken:', end_time - start)

if __name__ == '__main__':
    asyncio.run(main())