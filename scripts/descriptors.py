"""
A descriptor in Python is an object that defines how attributes are accessed and manipulated,
typically through __get__, __set__, and __delete__ methods
"""
import math


class PositiveNumber:
    def __set_name__(self, owner, name):
        """
        This is called when the descriptor (PositiveNumber object) is created. So it is called before __init__.
        """
        print(f"self = {self} __set_name__ with owner = {owner} and name = {name}")
        self._name = name

    def __get__(self, instance, owner):
        print(f"__get__ with instance = {instance} and owner = {owner}")
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        print(f"__set__ with instance = {instance} and value = {value}. self._name = {self._name}")
        if not isinstance(value, int | float) or value <= 0:
            raise ValueError("positive number expected")
        instance.__dict__[self._name] = value

class Circle:
    radius = PositiveNumber()

    def __init__(self, radiuss):
        self.radius = radiuss

    def calculate_area(self):
        return math.pi * self.radius**2


circle = Circle(3)
print(circle.calculate_area())
print(circle)
# circle.radius = -1
# print(circle.radius)
# print(Circle.radius._name)

import logging

logging.basicConfig(level=logging.INFO)

class LoggedAccess:

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.private_name)
        logging.info('Accessing %r giving %r', self.public_name, value)
        return value

    def __set__(self, obj, value):
        logging.info('Updating %r to %r', self.public_name, value)
        setattr(obj, self.private_name, value)

class Person:

    name = LoggedAccess()                # First descriptor instance
    age = LoggedAccess()                 # Second descriptor instance

    def __init__(self, name, age):
        self.name = name                 # Calls the first descriptor
        self.age = age                   # Calls the second descriptor

    def birthday(self):
        self.age += 1

# Vasile = Person("Vasile", 10)
# Vasile.birthday()
# print(Vasile.age)
