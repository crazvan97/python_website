def fibonacci(elem):
    if elem <= 1:
        return 0
    elif elem == 2:
        return 1
    else:
        return fibonacci(elem - 1) + fibonacci(elem - 2)

for i in range(10):
    print(fibonacci(i))