class Cat:
    def __init__(self, name):
        print("init")
        self._name = name

    @property
    def name(self):
        """Return the cat name"""
        print("getter")
        return self._name
        # return " ".join(["Hello", self._name])

    @name.setter
    def name(self, name):
        self._name = " ".join(["Hello", name])

petrica = Cat("Petrica")
print(petrica.name)