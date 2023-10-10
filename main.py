import time

from multiprocessing import Queue

from WikiWorker import WikiWorker
from YahooFinanceWorker import YahooFinancePriceScheduler
from SQLiteWorker import SQLLiteScheduler


def main():
    symbol_queue = Queue()
    sqlite_queue = Queue()
    scraper_start_time = time.time()

    wiki_worker = WikiWorker()
    yahoo_finance_price_scheduler_threads = []
    num_workers = 4
    for i in range(num_workers):
        yahoo_finance_price_scheduler = YahooFinancePriceScheduler(symbol_queue=symbol_queue, output_queue=[sqlite_queue])
        yahoo_finance_price_scheduler_threads.append(yahoo_finance_price_scheduler)

    sqlite_scheduler_threads = []
    num_sqlite_workers = 2
    for i in range(num_sqlite_workers):
        postgres_scheduler = SQLLiteScheduler(sqlite_queue=sqlite_queue)
        sqlite_scheduler_threads.append(postgres_scheduler)

    for symbol in wiki_worker.get_sp_500_companies():
        symbol_queue.put(symbol)

    for symbol in range(len(yahoo_finance_price_scheduler_threads)):
        symbol_queue.put('DONE')

    for symbol in range(len(yahoo_finance_price_scheduler_threads)):
        yahoo_finance_price_scheduler_threads[symbol].join()

    print('Extracting time taken:', time.time() - scraper_start_time)


if __name__ == '__main__':
    main()
