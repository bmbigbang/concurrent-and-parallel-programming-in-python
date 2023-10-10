from multiprocessing import Pool, cpu_count
from functools import partial


def square(y, add, x):
    return x ** y + add


num_processes = 4
comparison_list = [1, 2, 3]
power = 3
add = 2

num_cpu_to_use = max(1, cpu_count() - 1)

print('Number of cpus being used:', num_cpu_to_use)

partial_function = partial(square, power, add)

if __name__ == '__main__':
    with Pool(num_cpu_to_use) as p:
        result = p.map(partial_function, comparison_list)

    print(result)
