from multiprocessing import Pool, cpu_count
from functools import partial


def square(add, x, y):
    return x ** y + add


num_processes = 4
comparison_list = [1, 2, 3]
power_list = [4, 5, 6]
add = 2

num_cpu_to_use = max(1, cpu_count() - 1)

print('Number of cpus being used:', num_cpu_to_use)

partial_function = partial(square, add)

if __name__ == '__main__':
    with Pool(num_cpu_to_use) as p:
        result = p.starmap(partial_function, zip(comparison_list, power_list))

    print(result)
