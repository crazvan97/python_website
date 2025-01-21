# int
a = 1
# float
b = 2.5
# boolean
c = True
# string / bytes
d = "decorator"
d = d[0:2] + "co" + d[2:]
# print(d)
# tuple
e = (1, 2, 3)

ee = (1, 3, 2)
print(e.__hash__())
print(ee.__hash__())

lista = [1, 2, 3]
f = (lista, "ceva")
f[0][1] = 5
# print(f)

g = b'12345'
# print(type(g))
# print(ord(b'a'))

sett = {1, 2, 3}

dictio = {
    "cevapi": 3,
    f: 2
}
print(dictio)
