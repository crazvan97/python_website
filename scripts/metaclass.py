class SingletonMeta(type):
    _instances = {}

    def __new__(cls, name, bases, dct):
        print(f"Creating class: {name}")
        # Call the original metaclass's __new__ to create the class
        new_class = super().__new__(cls, name, bases, dct)
        return new_class

    def __call__(cls, *args, **kwargs):
        print(f"Attempting to instantiate: {cls.__name__}")
        if cls not in cls._instances:
            print(f"Creating new instance of {cls.__name__}")
            # If instance does not exist, create it using the class's __new__ method
            cls._instances[cls] = super().__call__(*args, **kwargs)
        else:
            print(f"Returning existing instance of {cls.__name__}")
        return cls._instances[cls]


class MyLogger(metaclass=SingletonMeta):
    def __new__(cls, *args, **kwargs):
        print(f"Executing __new__ for {cls.__name__}")
        # Custom behavior for __new__ can be added here
        instance = super().__new__(cls)
        return instance

    def __init__(self, value):
        print(f"Executing __init__ for {self.__class__.__name__}")
        self.value = value

    def __call__(self):
        print(f"Executing __call__ for {self.__class__.__name__}")
        return self.value


# Create instances of MyLogger
print("First instance creation:")
logger1 = MyLogger(42)  # This will invoke __new__, __init__, and __call__

print("\nSecond instance creation:")
logger2 = MyLogger(100)  # This will invoke __call__ and return the same instance

print("\nAre both instances the same?", logger1 is logger2)  # Should be True

print("\nCalling the logger instance:")
print(logger1())  # Calls __call__ and returns the value
