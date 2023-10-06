import time

from multiprocessing import Queue

from WikiWorker import WikiWorker
from YahooFinanceWorker import YahooFinancePriceWorker, YahooFinancePriceScheduler


def main():
    symbol_queue = Queue()
    scraper_start_time = time.time()

    wiki_worker = WikiWorker()
    yahoo_finance_price_scheduler_threads = []
    num_workers = 4
    for i in range(num_workers):
        yahoo_finance_price_scheduler = YahooFinancePriceScheduler(symbol_queue=symbol_queue)
        yahoo_finance_price_scheduler_threads.append(yahoo_finance_price_scheduler)

    for symbol in wiki_worker.get_sp_500_companies():
        symbol_queue.put(symbol)

    for symbol in range(len(yahoo_finance_price_scheduler_threads)):
        symbol_queue.put('DONE')

    for symbol in range(len(yahoo_finance_price_scheduler_threads)):
        yahoo_finance_price_scheduler_threads[symbol].join()

    print('Extracting time taken:', time.time() - scraper_start_time)


if __name__ == '__main__':
    main()
