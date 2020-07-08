

def fnv1(string, size=64):
    """
    FNV-1 Hash, 64-bit
    """
    FNV_PRIMES = {
        32: 16777619,
        64: 1099511628211,
        128: 309485009821345068724781371,
        256: 374144419156711147060143317175368453031918731002211,
    }

    FNV_OFFSET_BASIS = {
        32: 2166136261,
        64: 14695981039346656037,
        128: 144066263297769815596495629667062367629,
        256: 100029257958052580907070968620625704837092796014241193945225284501741471925557,
    }

    fnv_prime = FNV_PRIMES[size]
    fnv_offset_basis = FNV_OFFSET_BASIS[size]

    h = fnv_offset_basis

    for l in string:
        h = h ^ ord(l)
        h = h * fnv_prime
        # Missing octet breakup.  ord(l) produces 20bit memory al

    return h



def djb2(string):
    """
    DJB2 hash, 32-bit
    """
    h = 5381
    
    for l in string:
        h = (h << 5) + h + ord(l)

    return h





if __name__ == "__main__":
    print('fnv1')
    print(fnv1('test'), fnv1('tst'))

    print('djb2')
    print(djb2('test'), djb2('tst'))