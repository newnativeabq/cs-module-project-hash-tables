# Use frequency analysis to find the key to ciphertext.txt, and then
# decode it.

# Your code here

def read_file(path):
    with open(path, 'r') as file:
        t = file.read()
    return t


def _update_dict(dictionary, key, val):
    try:
        dictionary[key] += val
    except:
        if key.isalpha():
            dictionary[key] = val


def count_letters(string):
    letters = {}
    count = 0

    for letter in string:
        _update_dict(letters, letter, 1)
        if letter.isalpha():
            count += 1

    return letters, count


def count_to_freq(counts, total):
    for key in counts:
        counts[key] = counts[key] / total * 100
    return counts


SORTED_LETTERS = ('E', 'T', 'A', 'O', 'H', 'N', 'R', 'I', 'S', 'D', 'L', 'W', 'U',
'G', 'F', 'B', 'M', 'Y', 'C', 'P', 'K', 'V', 'Q', 'J', 'X', 'Z')


def sort_by_freq(f):
    flist = [(k, f[k]) for k in f]
    return [x[0] for x in sorted(flist, key=lambda x: x[1], reverse=True)]


def create_lookup_from_sorted(sorted_list):
    lookup = {}
    for k, v in zip(sorted_list, SORTED_LETTERS):
        lookup[k] = v
    return lookup


def decode(raw, cipher):
    message = ''

    for l in raw:
        if l in cipher.keys():
            message += cipher[l]
        else:
            message += l
    
    return message



if __name__ == "__main__":
    raw = read_file('ciphertext.txt')
    counts, total = count_letters(raw)
    freq = count_to_freq(counts, total)
    fsort = sort_by_freq(freq)
    lookup = create_lookup_from_sorted(fsort)
    message = decode(raw, lookup)
    print(message)