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


def _clean_word(word):
    word = word.lower()
    cword = ''.join([c for c in word if c.isalpha()])
    return cword


def count_letters(string):
    words = {}
    count = 0

    for word in string.split(' '):
        cword = _clean_word(word)
        _update_dict(words, cword, 1)
        if cword.isalpha():
            count += 1

    return words, count


def sort_by_freq(f):
    flist = [(k, f[k]) for k in f]
    return [x for x in sorted(flist, key=lambda x: x[1], reverse=True)]


def _draw_hash_from_pair(pair):
    return (pair[0], '#'*pair[1])


def gen_histogram(slist):
    return [
        _draw_hash_from_pair(pair) for pair in slist
    ]


def pretty_print(histogram, spacing=10):
    lpad = max([len(item[0]) for item in histogram])
    drawdist = spacing + lpad

    for item in histogram:
        spaces = drawdist - len(item[0])
        print(item[0], ' '*spaces, item[1])



if __name__ == "__main__":
    raw = read_file('robin.txt')
    counts, total = count_letters(raw)
    sorted_words = sort_by_freq(counts)
    histogram = gen_histogram(sorted_words)
    pretty_print(histogram)