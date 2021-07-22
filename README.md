# cuckoo-hash-table

This data structure is a type of hash table that provides an alternative solution to collisions without the use of separate chaining.
Cuckoo hashes utilize two hash functions to generate two hash tables. Keys can therefore be found in one of two possible locations: in hash table 1 or hash table 2.
If a key being inserted is hashed, and that position is occupied, it is rehashed using the second hash function and placed into hash table two. If that position is also occupied, the key that was already stored there is ejected and rehashed using the first hash function. This process of ejecting and rehashing is repeated until an empty position is found.
