from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def sound(self):
        pass

    @abstractmethod
    def move(self):
        pass


class Dog(Animal):
    def sound(self):
        print("Woof!")

    def move(self):
        print("The dog runs.")


class Bird(Animal):
    def sound(self):
        print("Chirp!")

    def move(self):
        print("The bird flies.")


# Create instances of concrete classes
dog = Dog()
dog.sound()  # Output: Woof!
dog.move()   # Output: The dog runs.

bird = Bird()
bird.sound()  # Output: Chirp!
bird.move()   # Output: The bird flies.
