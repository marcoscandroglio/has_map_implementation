# Name: Marco Scandroglio
# OSU Email: scandrom@oregonstate.com
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap (Portfolio Assignment)
# Due Date: 03/17/2023
# Description: This is the implementation of a Hash Map with Open addressing and Quadratic Probing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        A method that takes as parameters a key-value pair and inserts it into the hash table.
        The method checks that the current load factor is less than or equal to 0.5 and if not,
        calls the resize_table() method.  The method uses quadratic probing to search for either
        an empty bucket, one that has a tombstone flag, or one with a matching key.
        :param key: string
        :param value: object
        :return: None
        """

        # check load factor of the hash table and call resize_table() if necessary
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # calculate hash value and initial index value
        hash_value = self._hash_function(key)
        initial_index = hash_value % self._capacity
        new_index = initial_index
        j = 1

        # loop to traverse occupied buckets and check if they meet conditions to be updated
        while self._buckets[new_index] is not None:

            # matching key and not tombstone gets value updated without changing hash table size
            if self._buckets[new_index].key == key and not self._buckets[new_index].is_tombstone:
                self._buckets[new_index].value = value
                return

            # a bucket that is flagged as a tombstone gets replaced
            if self._buckets[new_index].is_tombstone:
                self._buckets[new_index] = HashEntry(key, value)
                self._size += 1
                return

            # calculate next index
            new_index = (initial_index + (j ** 2)) % self._capacity
            j += 1

        # if initial index bucket is empty create new hash entry
        if self._buckets[initial_index] is None:
            self._buckets[initial_index] = HashEntry(key, value)
            self._size += 1

        # if none of the occupied buckets could be updated or replaced create new hash entry in next open bucket
        elif self._buckets[new_index] is None:
            self._buckets[new_index] = HashEntry(key, value)
            self._size += 1

    def table_load(self) -> float:
        """
        A method that return the current table load by dividing the number of elements in the table
        by the number of buckets in the table.
        :return: float
        """

        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        A method that calculates and returns the number of empty buckets in the hash table
        by taking the difference between the number of buckets and the number of elements
        in the hash table.
        :return: integer
        """

        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        A method that takes as a parameter an integer representing a new capacity
        and resizes the hash table based on this new capacity.  It starts by
        validating that the new capacity is greater than or equal to the current
        hash table size.  Then it saves an array of the key value pairs, clears
        the table, recalculates the table load and adjusts the capacity as necessary,
        checks if the new capacity is prime and adjusts if necessary, adjusts number of
        buckets based on capacity, and finally rehashes all the saved key value
        pairs into the new hash table.
        :param new_capacity: integer
        :return: None
        """

        # validate new capacity
        if new_capacity >= self._size:

            # preserve key value elements
            old_buckets = self.get_keys_and_values()
            capacity = self._capacity

            # clear HashMap
            self.clear()

            # recalculate table load
            table_load = self._size / new_capacity

            # adjust capacity until table load is <= 0.5
            while table_load > 0.5:

                new_capacity = new_capacity * 2

                if not self._is_prime(new_capacity):
                    new_capacity = self._next_prime(new_capacity)

                table_load = self._size / new_capacity

            # check if new capacity is prime and modify if necessary
            # update capacity attribute
            if self._is_prime(new_capacity):
                self._capacity = new_capacity
            else:
                self._capacity = self._next_prime(new_capacity)

            # modify number of buckets based on the above
            # add buckets
            if self._capacity > capacity:

                for _ in range(capacity, self._capacity):
                    self._buckets.append(None)
            # remove buckets
            else:

                for _ in range(capacity - self._capacity):
                    self._buckets.pop()

            # rehash values into new hash table
            for i in range(old_buckets.length()):
                self.put(old_buckets[i][0], old_buckets[i][1])

    def get(self, key: str) -> object:
        """
        A method that takes as a parameter a key and, if the hash table is not empty,
        calculates the hash value and initial index of the key.  Quadratic probing
        is used if the key is not located at the first bucket.  If the key is found
        the method returns the value of the hash entry and if it is not found the
        method returns None.
        :param key: string
        :return: object
        """

        # check current size and return if empty
        if self.get_size() == 0:
            return

        # calculate hash value and initial index
        hash_value = self._hash_function(key)
        initial_index = hash_value % self._capacity
        new_index = initial_index
        j = 1

        # loop through hash table until key is found
        while self._buckets[new_index] is not None:

            if self._buckets[new_index].key == key and not self._buckets[new_index].is_tombstone:
                return self._buckets[new_index].value

            new_index = (initial_index + (j ** 2)) % self._capacity
            j += 1

    def contains_key(self, key: str) -> bool:
        """
        A method that takes as a parameter a key and, if the hash table is not empty,
        calculates the hash value and initial index of the key.  Quadratic probing
        is used if the key is not located at the first bucket.  If the key is found
        the method returns True and if it is not found the method returns False.
        :param key: string
        :return: boolean
        """

        # check current size and return False if empty
        if self.get_size() == 0:
            return False

        # calculate hash value and initial index
        hash_value = self._hash_function(key)
        initial_index = hash_value % self._capacity
        new_index = initial_index
        j = 1

        # loop through hash table until key is found
        while self._buckets[new_index] is not None:

            if self._buckets[new_index].key == key and not self._buckets[new_index].is_tombstone:
                return True

            new_index = (initial_index + (j ** 2)) % self._capacity
            j += 1

        # return False if key is not found
        return False

    def remove(self, key: str) -> None:
        """
        A method that takes as a parameter a key and, if the hash table is not empty,
        calculates the hash value and initial index of the key.  Quadratic probing
        is used if the key is not located at the first bucket.  If the key is found
        the method flags the hash entry as a tombstone and decrements the size
        attribute of the hash table.  If the key is not found the method does nothing.
        :param key: string
        :return: None
        """

        if self.contains_key(key):

            # calculate hash value and initial index
            hash_value = self._hash_function(key)
            initial_index = hash_value % self._capacity
            new_index = initial_index
            j = 1

            # loop through hash table until key is found
            while self._buckets[new_index] is not None:

                if self._buckets[new_index].key == key:
                    self._buckets[new_index].is_tombstone = True
                    self._size -= 1
                    return

                new_index = (initial_index + (j ** 2)) % self._capacity
                j += 1

    def clear(self) -> None:
        """
        A method that reinitialized the hash map using its current capacity and hash function.
        This method results in a cleared hash table of the same size.
        :return: None
        """

        self.__init__(self._capacity, self._hash_function)

    def get_keys_and_values(self) -> DynamicArray:
        """
        A method that iterates through the hash table and copies buckets
        containing key value pairs that are not marked as tombstones
        into a new DynamicArray that is returned by the method.
        :return: DynamicArray
        """

        # create new DynamicArray
        keys_values_arr = DynamicArray()

        # loop through buckets and append tuples of valid key value pairs to new array
        for i in range(self.get_capacity()):

            if self._buckets[i] is not None and not self._buckets[i].is_tombstone:
                keys_values_arr.append((self._buckets[i].key, self._buckets[i].value))

        return keys_values_arr

    def __iter__(self):
        """
        Returns an iterator object for the HashMap.
        :return: self
        """

        self._index = 0

        return self

    def __next__(self):
        """
        Returns the next item in the HashMap.  If the index is less than the capacity
        and the index is None or has a tombstone flag this method increments to the
        next index until either the next item is found ir a StopIteration is raised.
        :return: value object
        """

        # checks that index is less than capacity and skips empty and tombstone buckets
        while self._index < self._capacity and (self._buckets[self._index] is None or self._buckets[self._index].is_tombstone):
            self._index += 1

        if self._index == self._capacity:
            raise StopIteration

        # assigns value and increments index
        value = self._buckets[self._index]
        self._index += 1

        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
