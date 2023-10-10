from multiprocessing import Process, Queue

import time


def check_value_in_list(x, i, number_of_processes, queue):
    max_number_to_check_to = 10**8
    lower = int(i * max_number_to_check_to / number_of_processes)
    upper = int((i + 1) * max_number_to_check_to / number_of_processes)
    count = 0
    for i in range(lower, upper):
        if i in x:
            count += 1

    queue.put((lower, upper, count))

num_processes = 8
comparison_list = [1, 2, 3]

if __name__ == '__main__':
    start_time = time.time()
    queue = Queue()
    processes = []
    for i in range(num_processes):
        t = Process(target=check_value_in_list, args=(comparison_list, i, num_processes, queue))
        processes.append(t)

    for t in processes:
        t.start()

    for t in processes:
        t.join()

    queue.put('DONE')

    while True:
        v = queue.get()
        if v == 'DONE':
            break
        lower, upper, count = v
        print('Between', lower, ' and ', upper, 'we have', count, 'matching values in the list')
    print('With multiprocessing it took:', time.time() - start_time, 'seconds')