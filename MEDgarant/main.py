import numpy as np
import time
import collections


def slow_alg(low, high, size, numbers = None):
    result = []
    if numbers == None:
        numbers = list(np.random.randint(low=low, high=high, size=size))
    start_time = time.time()
    
    for i, number in enumerate(numbers):
        result.append(number in numbers[i+1:])

    print('Slow algoritm:', time.time() - start_time, 'seconds')
    return result
    
    
def fast_alg(low, high, size, numbers = None):
    result = []
    if numbers == None:
        numbers = list(np.random.randint(low=low, high=high, size=size))
    start_time = time.time()
    
    all_numbers = {i: 0 for i  in range(low, high)}
    for i in range(size):
        all_numbers[numbers[i]] += 1

    for i in range(size):
        if all_numbers[numbers[i]] > 1:
            all_numbers[numbers[i]] -= 1
            result.append(True)
        else:
            result.append(False)

    print('Fast algoritm:', time.time() - start_time, 'seconds')
    return result
    
    
if __name__ == '__main__':
    low_ = 1
    high_ = 10
    size_ = 100000
    for i in range(5):
        numbers_ = list(np.random.randint(low=low_, high=high_, size=size_))
        sa = slow_alg(low_, high_, size_, numbers=numbers_)
        fa = fast_alg(low_, high_, size_, numbers=numbers_)
        if collections.Counter(sa) == collections.Counter(fa):
            print('Equal results\n')
        else:
            print('! Unequal results !\n')
