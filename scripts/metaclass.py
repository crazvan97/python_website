"""
A metaclass is a class that defines the behavior of other classes.
It controls how classes are created and can be used to modify the class structure, add attributes, or enforce rules.
The default metaclass is type, but you can define your own to customize class creation.
"""

class Creatura(type):
    def __instancecheck__(cls, instance):
        print(instance)
        print(type(instance))
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return hasattr(subclass, "age") and callable(subclass.age)

class Person(metaclass=Creatura):
    pass

class Ion:
    def age(self):
        print("age")

class Ion2:
    def agew(self):
        print("age")

# print(type(Ion))
# print(type(Person))
print(issubclass(Ion, Person))
print(issubclass(Ion2, Person))

print(isinstance(Ion, Person))
print(isinstance(Ion2, Person))
print(Ion.__mro__)

from abc import ABCMeta, abstractmethod

class Pisoi(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, __subclass):
        return hasattr(__subclass, "mew") and callable(__subclass.mew)

    @abstractmethod
    def mew(self):
       raise NotImplementedError

class Rebel(Pisoi):
    def __init__(self):
        self.name = "Vagabont"

    def mew(self):
        raise NotImplementedError

reb = Rebel()