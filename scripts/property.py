"""
A property in Python is a built-in descriptor that allows you to define getter, setter, and deleter methods
for an attribute in a class
"""
class Cat:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """Return the cat name"""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @name.deleter
    def name(self):
        print("acum se sterge")
        del self._name

    def say_hello(self):
        print(f"Say hello to {self.name}")

petrica = Cat("Petrica")
print(petrica.name)

petrica.name = "Vasile"
print(petrica.name)

petrica.say_hello()

del petrica.name