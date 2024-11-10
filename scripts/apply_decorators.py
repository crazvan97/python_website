import math
import time

from scripts.decorators import time_duration, add_timestamp


@time_duration
def factorial(n):
    time.sleep(n)
    return math.factorial(n)

@add_timestamp
def print_message():
    return "any message"


print(factorial(2))
print_message()
