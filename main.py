import time

from WikiWorker import WikiWorker
from YahooFinanceWorker import YahooFinancePriceWorker


def main():
    scraper_start_time = time.time()
    wikiWorker = WikiWorker()
    symbol_list = [i for i in wikiWorker.get_sp_500_companies()]
    current_threads = {}

    for symbol in set(symbol_list[:10]):
        worker = YahooFinancePriceWorker(symbol=symbol)
        current_threads[symbol] = worker
        time.sleep(0.2)

    for symbol in current_threads.keys():
        current_threads[symbol].join()
        print(symbol, current_threads[symbol].get_price())

    print('Extracting time taken:', time.time() - scraper_start_time)


if __name__ == '__main__':
    main()
