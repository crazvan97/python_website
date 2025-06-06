class A:
    def __init__(self):
        self._attr = 0

    def __method(self):
        print("A.__attr", self._attr)

class B(A):
    def __init__(self):
        super().__init__()
        self._attr = 1

    def __method(self):  # Doesn't override A.__method()
        print("B.__attr", self._attr)

a = A()
b = B()
b._A__method()

print(vars(a))
print(vars(b))