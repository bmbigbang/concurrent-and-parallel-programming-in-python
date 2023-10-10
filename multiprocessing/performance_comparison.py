from multiprocessing import Process
from threading import Thread

import time


def check_value_in_list(x):
    for i in range(10**8):
        i in x


num_processes = 8
comparison_list = [1, 2, 3]

if __name__ == '__main__':
    start_time = time.time()
    threads = []
    for i in range(num_processes):
        t = Thread(target=check_value_in_list, args=(comparison_list,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print('With threading it took:', time.time() - start_time, 'seconds')

    start_time = time.time()
    processes = []
    for i in range(num_processes):
        t = Process(target=check_value_in_list, args=(comparison_list,))
        processes.append(t)

    for t in processes:
        t.start()

    for t in processes:
        t.join()

    print('With multiprocessing it took:', time.time() - start_time, 'seconds')