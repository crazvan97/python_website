class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class MyClass(metaclass=Singleton):
    def __init__(self, marc):
        self.marc = marc
        print("init")

c1 = MyClass("toy")
c2 = MyClass("vw")

class MyNewClass(metaclass=Singleton):
    def __init__(self, marc):
        self.marc = marc
        print("new init")

c3 = MyNewClass("dacia")
c4 = MyNewClass("bmw")

print(c1.marc)
print(c2.marc)
print(c3.marc)
print(c4.marc)