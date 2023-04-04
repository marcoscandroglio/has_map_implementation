# Name: Marco Scandroglio
# OSU Email: scandrom@oregonstate.com
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap (Portfolio Assignment)
# Due Date: 03/17/2023
# Description: This is the implementation of a Hash Map with Separate Chaining

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        The method checks that the current load factor is less than or equal to 1.0 and if not,
        calls the resize_table() method.  The method uses separate chaining and checks if the
        linked list at the index already has the key being inserted and updates its value.
        If the key is not in the linked list the new key value pair is inserted/
        :param key: string
        :param value: object
        :return: None
        """

        # check load factor of the hash table and call resize_table() if necessary
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        # calculate hash value and initial index value
        hash_value = self._hash_function(key)
        initial_index = hash_value % self._buckets.length()
        ll_at_index = self._buckets[initial_index]
        key_at_index = ll_at_index.contains(key)

        # if the key already exists the value is updated otherwise the new key value pair is inserted
        if key_at_index:
            key_at_index.value = value

        else:
            ll_at_index.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        A method that counts the number of empty buckets in the hash table by iterating
        over the buckets and keeping a count of the ones that have linked lists with
        lengths equal to 0.
        :return: integer
        """

        # set bucket counter
        buckets = 0

        # iterate over buckets
        for i in range(self._buckets.length()):

            if self._buckets[i].length() == 0:
                buckets += 1

        return buckets

    def table_load(self) -> float:
        """
        A method that return the current table load by dividing the number of elements in the table
        by the number of buckets in the table.
        :return: float
        """

        return self.get_size() / self.get_capacity()

    def clear(self) -> None:
        """
        A method that reinitialized the hash map using its current capacity and hash function.
        This method results in a cleared hash table of the same size.
        :return: None
        """

        self.__init__(self._capacity, self._hash_function)

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

        if new_capacity >= 1:

            # preserve key value elements
            cur_buckets = self.get_keys_and_values()

            # capacity must be a prime number
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)

            # recalculate table load
            table_load = self._size / new_capacity

            # adjust capacity until table load is <= 1.0
            while table_load > 1.0:

                new_capacity = new_capacity * 2

                if not self._is_prime(new_capacity):
                    new_capacity = self._next_prime(new_capacity)

                table_load = self._size / new_capacity

            # assign new capacity to attribute
            self._capacity = new_capacity

            # create an empty hash table
            new_buckets = DynamicArray()

            for i in range(self._capacity):
                new_buckets.append(LinkedList())

            # assign new hash table to attribute
            self._buckets = new_buckets
            self._size = 0

            # rehash values into new hash table
            for i in range(cur_buckets.length()):
                key, value = cur_buckets[i]
                self.put(key, value)

    def get(self, key: str):
        """
        A method that takes as a parameter a key and, if the hash table is not empty,
        calculates the hash value and index of the key.  If the key is found
        the method returns the value of the node and if it is not found the
        method returns None.
        :param key: string
        :return: object
        """

        if self.get_size() > 0:

            # calculate index and get node value if it exists
            hash_value = self._hash_function(key)
            index = hash_value % self._capacity
            node = self._buckets[index].contains(key)

            # if node exists return the value
            if node:
                return node.value

    def contains_key(self, key: str) -> bool:
        """
        A method that takes as a parameter a key and, if the hash table is not empty,
        calculates the hash value and index of the key.  If the key is found
        the method returns True and if it is not found the method returns False.
        :param key: string
        :return: boolean
        """

        # checks if hash table is empty
        if self.get_size() > 0:

            # calculate index
            hash_value = self._hash_function(key)
            index = hash_value % self._capacity

            # checks for presence of node and matching key value
            if self._buckets[index].contains(key) and self._buckets[index].contains(key).key == key:
                return True

        return False

    def remove(self, key: str) -> None:
        """
        A method that takes as a parameter a key and, if the hash table is not empty,
        calculates the hash value and index of the key.  If the key is found
        the method removes the entry from the linked list and decrements the size
        attribute of the hash table.  If the key is not found the method does nothing.
        :param key: string
        :return: None
        """

        # calculate index
        hash = self._hash_function(key)
        index = hash % self._capacity

        # if key value was removed decrement size
        if self._buckets[index].remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        A method that iterates through the hash table and copies buckets containing
        key value pairs into a new DynamicArray that is returned by the method.
        :return: DynamicArray
        """

        # create new DynamicArray
        keys_values_arr = DynamicArray()

        # iterate through buckets and if a bucket contains values copy them to the new array
        for i in range(self.get_capacity()):
            if self._buckets[i].length() > 0:
                for j in self._buckets[i]:
                    keys_values_arr.append((j.key, j.value))

        return keys_values_arr


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    A function that takes as a parameter a DynamicArray and returns a tuple
    containing a DynamicArray containing the value(s) that are the mode of
    the parameter array and an integer representing the frequency of the mode.
    O(n) runtime complexity.
    :param da: DynamicArray
    :return: tuple (DynamicArray, int)
    """

    # create new HashMap()
    map = HashMap()

    # loop through the parameter array and add values to the hash map
    # the values in the parameter array are keys in the hash map
    # and the value associated with each key in the hash map is the
    # frequency of the key in the parameter array
    for i in range(da.length()):

        key = da[i]
        cur_value = map.get(key)

        # if key already exists put key with incremented value
        if cur_value:
            map.put(key, cur_value + 1)

        # add key with value of 1 if it does not exist in the HashMap
        else:
            map.put(key, 1)

    # extract key value pairs from HashMap and initialize new variable and DynamicArray
    key_value_list = map.get_keys_and_values()
    max_frequency = None
    mode_arr = DynamicArray()

    # iterate through list of key value pairs while looking for
    # key value pairs that have the highest value
    for i in range(key_value_list.length()):

        if max_frequency is None:
            max_frequency = key_value_list[i][1]

        # elements with equal frequency are recorded
        if key_value_list[i][1] == max_frequency:
            mode_arr.append(key_value_list[i][0])

        # overwrite array if elements with higher frequency are found
        if key_value_list[i][1] > max_frequency:
            max_frequency = key_value_list[i][1]
            mode_arr = DynamicArray()
            mode_arr.append(key_value_list[i][0])

    return mode_arr, max_frequency


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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
