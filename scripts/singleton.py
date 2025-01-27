class SingletonMeta(type):
    _instancess = {}
    def __call__(cls, *args, **kwargs):
        print(f"call {args}")
        if cls not in cls._instancess:
            cls._instancess[cls] = super().__call__(*args, **kwargs)
        return cls._instancess[cls]


class MyLogger(metaclass=SingletonMeta):
    def __new__(cls, *args, **kwargs):
        print("Debug: __new__ is called")
        return super(MyLogger, cls).__new__(cls)
    def __init__(self, param):
        print("init")
        self.param = param


#-------------------------------------------------------------------------
def singleton(cls):
    instances = {}
    def get_instace(*args, **kwargs):
        if cls not in instances:
            print(cls)
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instace


#FunctionDec = singleton(FunctionDec) -> get_instance
@singleton
class FunctionDec:
    def __init__(self, param):
        print("init")
        self.param = param

    def write_to_file(self):
        print(self.param)

