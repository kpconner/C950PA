# Hash table class for package objects.  Utilizes direct hashing with package objects IDs as keys.
class HashTable:
    # Initializes empty list of length specified by capacity
    def __init__(self, capacity):
        self.values = capacity * [None]

    def __len__(self):
        return len(self.values)

    # Inserts items/packages into values list using hash value of key modulo length of the list
    def insert_item(self, key, item):
        index = hash(key) % len(self)
        self.values[index] = item

    # Returns item from hash table values at index specified by key if the value at the index is not empty
    def get_item(self, key):
        index = hash(key) % len(self)
        if self.values[index] is not None:
            return self.values[index]
        else:
            return None

    # Removes items from the hash table if the index addressed by the key is not empty
    def remove_item(self, key):
        index = hash(key) % len(self)
        if self.values[index] is not None:
            self.values[index] = None
