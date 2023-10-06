import threading
import time

from WikiWorker import WikiWorker
from YahooFinanceWorker import YahooFinancePriceWorker


def calculate_sum_of_squares(n):
    return sum([j ** 2 for j in range(n)])


def main_old():
    calc_start_time = time.time()

    current_threads = []
    for i in range(5):
        maximum_value = (i + 1) * 1000000
        t = threading.Thread(target=calculate_sum_of_squares, args=(maximum_value,))
        t.start()
        current_threads.append(t)

    for i in range(len(current_threads)):
        current_threads[i].join()

    print('Calculating sum of squares took:', time.time() - calc_start_time)

    sleep_start_time = time.time()

    current_threads = []
    for seconds in range(1, 6):
        t = threading.Thread(target=lambda x: time.sleep(x), args=(seconds,))
        t.start()
        current_threads.append(t)

    for i in range(len(current_threads)):
        current_threads[i].join()

    print('sleep took:', time.time() - sleep_start_time)


def main():
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


if __name__ == '__main__':
    main()
