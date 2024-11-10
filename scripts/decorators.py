import time
import datetime


def time_duration(func):
    def inner(*args):
        start = time.time()
        output = func(*args)
        stop = time.time()
        print(f"Function {func.__name__} executed in {round(stop - start, 2)} seconds.")
        return output
    return inner


def add_timestamp(func):
    def inner():
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        output = func()
        print(f'[{timestamp}] {output} - {func.__name__}()')
    return inner
