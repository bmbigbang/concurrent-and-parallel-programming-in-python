import requests
import threading
import time

from bs4 import BeautifulSoup
from queue import Empty


class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self, symbol_queue, output_queue, **kwargs):
        super(YahooFinancePriceScheduler, self).__init__(**kwargs)
        self._symbol_queue = symbol_queue
        temp_queue = output_queue
        if type(temp_queue) != list:
            temp_queue = [temp_queue]
        self._output_queues = temp_queue
        self.start()

    def run(self):
        while True:
            try:
                val = self._symbol_queue.get()
            except Empty:
                print('Yahoo scheduler queue is empty')
                break

            if val == 'DONE':
                for output_queue in self._output_queues:
                    output_queue.put('DONE')
                break
            yahoo_finance_price_worker = YahooFinancePriceWorker(symbol=val)
            price = yahoo_finance_price_worker.get_price()
            for output_queue in self._output_queues:
                output_queue.put((val, float(price)))
            time.sleep(0.2)


class YahooFinancePriceWorker():
    def __init__(self, symbol):
        self._price = None
        self._symbol = symbol
        base_url = "https://uk.finance.yahoo.com/quote/"
        self._url = '{0}{1}'.format(base_url, self._symbol)

    def get_price(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': '<insert your cookie>'
        }
        response = requests.get(self._url, headers=headers)
        if response.status_code != 200:
            print("Couldn't get price")
            return 0
        soup = BeautifulSoup(response.text, "html.parser")
        price_element = soup.find(attrs={"data-test": "qsp-price"})
        return price_element.attrs["value"]
