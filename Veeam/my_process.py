import time
import random

array = []
counter = 100000

for i in range(int(counter)):
    array.append(time.time())
    if i > counter / 2:
        array.sort()

print('Process is end.')
