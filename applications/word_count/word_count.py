import re

def read_file(path):
    with open(path, 'r') as file:
        t = file.read()
    return t


def _update_dict(dictionary, key, val):
    try:
        dictionary[key] += val
    except:
        if (key is not None) and (len(key)>0):
            dictionary[key] = val


def _valid_char(char):
    if char not in '" : ; , . - + = / \ | [ ] { } ( ) * ^ &'.split():
        return char


def _coalesce(*args):
    for i in args:
        if i is not None:
            return i


def _clean_word(word):
    word = word.lower()
    cword = ''.join([_coalesce(_valid_char(c), '') for c in word])
    return cword


def split_string(string):
    items = []
    for item in string.split():
        for sub in item.split():
            items.append(sub)
    return items


def word_count(string):
    words = {}
    count = 0

    for word in split_string(string):
        cword = _clean_word(word)
        _update_dict(words, cword, 1)

    return words

if __name__ == "__main__":
    print(word_count(""))
    print(word_count("Hello"))
    print(word_count('Hello, my cat. And my cat doesn\'t say "hello" back.'))
    print(word_count('This is a test of the emergency broadcast network. This is only a test.'))