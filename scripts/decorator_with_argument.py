def decorator_function_with_arguments(arg1, arg2, arg3):
    def wrap(f):
        print("Inside wrap()")
        def wrapped_f(*args):
            print("Inside wrapped_f()")
            print("Decorator arguments:", arg1, arg2, arg3)
            f(*args)
            print("After f(*args)")
        return wrapped_f
    return wrap

@decorator_function_with_arguments("hello", "world", 42)
def say_hello(a1, a2, a3, a4):
    print('say_hello arguments:', a1, a2, a3, a4)

print("After decoration")

print("Preparing to call say_hello()")
say_hello("say", "hello", "argument", "list")
print("after first say_hello() call")
say_hello("a", "different", "set of", "arguments")
print("after second say_hello() call")