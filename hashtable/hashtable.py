from hashfunctions import djb2, fnv1


class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __repr__(self):
        return f'{self.key}: {self.value}'


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity, hashfn = fnv1):
        # Your code here
        self.hashfn = hashfn
        self.capacity = capacity
        self.store = [None] * capacity


    def hash(self, key):
        return self.hashfn(key)


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return len(self.store)


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        c = sum([item is not None for item in self.store])
        return c / self.get_num_slots()


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        i = self.hash(key) % self.capacity
        return i


    def search_entries(self, e, k):
        t = e
        if t is None:
            return

        while True:
            if t.key == k:
                return t
            elif t.next is None:
                return t
            else:
                t = t.next


    def add_update(self, k, v):
        i = self.hash_index(k)
        t = self.store[i]

        if t is None:
            self.store[i] = HashTableEntry(k, v)
            return

        n = self.search_entries(t, k)
        if n.key == k:
            n.value = v 
        else:
            n.next = HashTableEntry(k,v)


    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        i = self.hash_index(key)
        self.add_update(key, value)


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        i = self.hash_index(key)
        e = self.search_entries(self.store[i], key)

        if e is None:
            print('Key not found')
        elif e.key != key:
            print('Key not found')
            return
        e.value = None


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        def _validate(e, k):
            assert e.key == k, 'Search failed'

        i = self.hash_index(key)
        e = self.search_entries(self.store[i], key)

        if e is None:
            return
        _validate(e, key) 
        return e.value


    def _get_all(self, swap):
        items = []
        for e in swap:
            t = e
            if t is not None:
                while True:
                    items.append((t.key, t.value))
                    if t.next is not None:
                        t = t.next
                    else:
                        break
        return items


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        swap = [item for item in self.store]
        self.store = [None] * new_capacity

        while len(swap) > 0:
            entry = swap.pop()
            if entry is not None:
                self.store[self.hash_index(entry.key)] = entry

        # [self.add_update(k, v) for k, v in self._get_all(swap)]



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
