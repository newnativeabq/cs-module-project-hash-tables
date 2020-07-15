# Your code here
import random 
import math


CACHE = {}

def cached(cache=CACHE):
    def check_args(func):
        def call(*args, **kwargs):
            if args in cache:
                return cache[args]
            else:
                result = func(*args)
                cache[args] = result
                return result
        return call 
    return check_args


@cached(CACHE)
def slowfun(x, y):
    v = math.pow(x, y)
    v = math.factorial(v)
    v //= (x + y)
    v %= 982451653

    return v


# Do not modify below this line!

for i in range(50000):
    x = random.randrange(2, 14)
    y = random.randrange(3, 6)
    print(f'{i}: {x},{y}: {slowfun(x, y)}')
