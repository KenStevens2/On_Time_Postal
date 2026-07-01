
# creates class HashTable
class HashTable:
    def __init__(self, size=50):
        self.table = []

        for i in range(size):
            self.table.append([])

    # adds an item to the table or updates an existing item
    def insert(self, key, value):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                key_value[1] = value
                return True

        key_value = (key, value)
        bucket_list.append(key_value)
        return True

    # returns the value of an item in the table
    def get(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]

        return None

    # removes an item from the hash table
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for key_value in bucket_list:
            if key_value[0] == key:
                bucket_list.remove(key_value)
                return True

        return False

    # prints the hash table
    def print_table(self):
        print(f"\n\n Hash Table \n\n")
        for bucket in self.table:
            if bucket:
                for key_value in bucket:
                    print(key_value[0], key_value[1])
