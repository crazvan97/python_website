def singleton(cls):
    instances = {}
    def get_instace(*args, **kwargs):
        if cls not in instances:
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

func = FunctionDec(1) # get_instance(1) -> cls -> FunctionDec
func2 = FunctionDec(2)