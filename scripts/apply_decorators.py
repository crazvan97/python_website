import math
import time

from scripts.decorators import time_duration, add_timestamp, start_stop, TimeDecorator

# factorial = time_duration(factorial)
@time_duration
def factorial(n):
    time.sleep(n)
    return math.factorial(n)

@add_timestamp
def print_message():
    return "any message"

@start_stop
def do_something(ceva):
    time.sleep(1)
    print(f"Do something {ceva}")

# print_ok = TimeDecorator(print_ok); print_ok() -> invoke __call__ from TimeDecorator
@TimeDecorator
def print_ok(param):
    return param


# print(factorial(2))
# print_message()
# do_something("bun")

print(print_ok("bun"))
