import random
import copy


"""
Markov Chain:

    Tokenized Chain-Set Implementation.
    Items are first tokenized and two frequency distributions are created;
        1. Token likelihood
        2. Type distribution (A distribution for each type of token to allow selection)
"""



## Helper Functions

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

## Main Objects & Methods

class Token():
    def __init__(self, value):
         self.value = value




class Punct(Token):
    """
    Includes punctuation and spaces
    """
    def __init__(self, value):
        super().__init__(value)
        self.type = 'punct'
    

    def __repr__(self):
        return f'<Punct> {self.value}'




class Word(Token):
    def __init__(self, value):
        super().__init__(value)
        self.type = 'word'
    

    def __repr__(self):
        return f'<Word> {self.value}'




class Doc():
    def __init__(self, data):
        self.data = data
        self._words = {}
        self._punct = {}
        self._entities = []


    def __repr__(self):
        return f'<Doc> \n {self._sample(self.data)}'
    

    def lookup(self, val):
        if val in self._words:
            return self._words[val]
        elif val in self._punct:
            return self._punct[val]
    

    def _sample(self, data, max_len=100):
        if len(data) <= max_len:
            return data
        return data[0:max_len]

    
    def _parse_item(self, item):
        t = [c for c in item.lower()]
        
        def is_punct(span):
            if span in self._punct:
                return True
            return False
        
        def is_word(span):
            if span in self._words:
                return True 
            return False
        
        def _pop_remaining_letters(t):
            newstring = ''
            while len(t) > 0:
                if t[0].isalpha():
                    newstring += t.pop(0)
                else:
                    break
            return newstring

        span = ''
        parsed = []
        while len(t) > 0:
            span += t.pop(0)
            if is_punct(span): 
                parsed.append(self._punct[span])
                span = ''
            elif is_word(span):
                span += _pop_remaining_letters(t)
                if is_word(span):
                    parsed.append(self._words[span])
                    span = ''

        return parsed



    def _identify(self, items):
        entities = []
        for item in items:
            components = self._parse_item(item)
            entities += components 
        return entities

    @property
    def punct(self):
        return list(self._punct.values())
    
    @property 
    def words(self):
        return list(self._words.values())

    @punct.setter
    def punct(self, punct):
        self._punct = punct
    
    @words.setter 
    def words(self, words):
        self._words = words


    @property 
    def entities(self):
        if len(self._entities) < 1:
            self._entities = self._identify(self.items)
        return self._entities



class Tokenizer():
    def __init__(self):
        pass


    def tokenize(self, filepath=None, string=None):
        if filepath is not None:
            data = self._load_file(filepath)
        elif string is not None:
            data = string

        doc = Doc(data)
        doc.items = split_string(doc.data)
        doc.words = self._identify_words(doc)
        doc.punct = self._identify_punct(doc)

        return doc


    def _identify_words(self, doc:Doc):
        items = doc.items
        words = {}
        for item in items:
            citem = _clean_word(item)
            if citem not in words:
                words[citem] = Word(citem)
        return words



    def _identify_punct(self, doc:Doc):
        items = doc.items
        puncts = {}
        for item in items:
            for c in item:
                if _valid_char(c) is None:
                    puncts[c] = Punct(c)
        return puncts


    def _load_file(self, filepath):
        return read_file(filepath)




## Markov Chain Construction

import numpy as np

class Distribution():
    def __init__(self, values:tuple, frequencies:tuple):
        assert len(values) == len(frequencies), 'Must provide one frequency per value in order'
        self.values = values 
        self.frequencies = frequencies

    def __repr__(self):
        return f'<Distribution> {self.values} {self.frequencies}'

    def sample(self, n):
        return np.random.choice(
            self.values, n, p=self.frequencies
        )
        

        

def build_distribution(entity, doc, focus):
    """ Build entity distribution of attribute type focus (word, punct, type) """
    dist = {}

    def _correct_type(entity, focus):
        return entity.type == focus

    def _get_next(iterable, index, focus):
        if (index + 1) < len(iterable):
            if (focus == 'type') or _correct_type(iterable[index+1], focus):
                return iterable[index+1]
        return False

    def _get_item(obj, focus):
        if focus == 'type':
            return obj.type
        return obj.value

    def _val_to_freq(dist):
        total = sum(list(dist.values()))
        for key in dist:
            dist[key] *= 1/total
        
        vals = tuple(dist.keys())
        freq = tuple(dist[val] for val in vals)
        return Distribution(vals, freq)



    for i, item in enumerate(doc.entities):
        next_item = _get_next(doc.entities, i, focus)
        if next_item:
            if item.value == entity.value:
                _update_dict(dist, _get_item(next_item, focus), 1)

    return _val_to_freq(dist)



def construct_entity_distributions(*args):
    entity, doc = args[0]
    punct_dist = build_distribution(entity, doc, 'punct')
    word_dist = build_distribution(entity, doc, 'word')
    type_dist = build_distribution(entity, doc, 'type')

    return  {
                entity.value:
                    {
                        'word': word_dist,
                        'punct': punct_dist,
                        'types': type_dist,
                    }
            }

def _collapse_tuple_dicts(iterable):
    """Assumes iterable of dicts"""
    temp = {}
    for i in iterable:
        temp.update(i)
    return temp


class Generator():
    def __init__(self, doc, distributions):
        self.doc = doc
        self.dists = distributions

    
    def __call__(self, item=None):
        if item is None:
            return np.random.choice(doc.words)

        def _get_single_type(item, dtype):
            try:
                dist = dists[item.value][dtype]
                val = dist.sample(1)[0]
                return val 
            except KeyError:
                return None
        
        def _get_single_val(item, dtype):
            try:
                dist = dists[item.value][dtype]
                val = dist.sample(1)[0]
                return self.doc.lookup(val)
            except KeyError:
                return None

        # Get a type choice
        next_type = _get_single_type(item, 'types')
        # Get an entity of next type
        return _get_single_val(item, next_type)


def generate_sequence(generator, n):
    g = generator
    seed = g()
    sequence = [seed]
    for i in range(n - 1):
        sequence.append(
            g(sequence[i-1])
        )
    return sequence


def pretty_print(sequence):
    pstr = ''

    for ent in sequence:
        if ent is not None:
            if ent.type == 'punct':
                pstr += ent.value
            else:
                pstr += f' {ent.value}'
    return pstr

if __name__ == "__main__":
    tk = Tokenizer()
    doc = tk.tokenize('input.txt')

    from multiprocessing import Pool
    with Pool(6) as p:
        dists = list(
            p.map(construct_entity_distributions, [(entity, doc) for entity in doc.entities])
        )
        dists = _collapse_tuple_dicts(dists)

    print(len(dists.keys()))

    g = Generator(doc, dists)

    for _ in range(5):
        print(pretty_print(generate_sequence(g, 20)))
