# Your code here

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
def expensive_seq(*args):
    x = args[0]
    y = args[1]
    z = args[2]

    if x <= 0: 
        return y + z
    if x >  0: 
        return expensive_seq(x-1,y+1,z) + expensive_seq(x-2,y+2,z*2) + expensive_seq(x-3,y+3,z*3)



if __name__ == "__main__":
    for i in range(10):
        x = expensive_seq(i*2, i*3, i*4)
        print(f"{i*2} {i*3} {i*4} = {x}")

    print(expensive_seq(150, 400, 800))
