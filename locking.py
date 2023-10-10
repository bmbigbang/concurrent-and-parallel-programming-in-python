import threading


counter = 0

lock = threading.Lock()


def increment_counter():
    global counter
    for _ in range(10**6):
        with lock:
            lock.acquire()
            counter += 1


threads = []
for i in range(4):
    x = threading.Thread(target=increment_counter)
    threads.append(x)

for t in threads:
    t.start()

for t in threads:
    t.join()

print('Counter value:', counter)