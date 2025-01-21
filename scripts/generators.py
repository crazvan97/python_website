"""
A generator in Python is a special type of iterator that allows you to iterate over a sequence of values.
A generator uses the yield keyword to return a value and pause its execution, allowing it to resume
from where it left off when the next value is requested.

An iterator is an object that allows you to traverse through all the elements in a collection one by one,
maintaining the current position in the collection and raising StopIteration when there are no more elements.
"""

class MyIterator:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self  # The iterator object itself

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration  # End of the iteration
        self.current += 1
        return self.current - 1


def my_generator(start, pas):
    # for i in sequence:
    #     yield i
    while True:
        start = start + pas
        yield start


# seq = my_generator([1, 2, 3])
seq = my_generator(0,1)
print(seq)
print(seq.__next__())
print(seq.__next__())
print(seq.__next__())
print(seq.__next__())
print(seq.__next__())
