"""
find all a, b, c, d in q such that
f(a) + f(b) = f(c) - f(d)
"""
import copy

def cached(cache):
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




#q = set(range(1, 10))
#q = set(range(1, 200))
q = (1, 3, 4, 7, 12)


def f(x):
    return x * 4 + 6



def find_sums(q):
    sums = {}
    for c, i in enumerate(q):
        temp = list(q)
        temp.pop(c)
        for j in temp:
            sums[(i,j)] = f(i) + f(j)  # can be made more efficient since add is symmetric
    return sums


def find_diffs(q):
    diffs = {}
    for c, i in enumerate(q):
        temp = list(q)
        temp.pop(c)
        for j in temp:
            diffs[(i,j)] = f(i) - f(j)
    return diffs


def invert_dict(ht):
    iht = {}
    for key in ht:
        newkey = ht[key] 
        if newkey in iht:
            iht[newkey] = iht[newkey] + [key]
        else:
            iht[newkey] = [key]
    return iht


def match_keys(isums, idiffs):
    matches = []
    for sums in isums:
        if sums in idiffs:
            matches.append(
                (isums[sums], idiffs[sums])
            )
    return matches


# Your code here

if __name__ == "__main__":
    sums = find_sums(q+q)  # summationi to allow for repeat picking
    diffs = find_diffs(q+q)

    isums = invert_dict(sums)
    idiffs = invert_dict(diffs)
    
    matched_quants = match_keys(isums, idiffs)
    
    for quants in matched_quants:
        print(quants[0], ' = ', quants[1])