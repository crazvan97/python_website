"""
Mutable types: list, dict, set, bytearray. -> their values can be updated or modified
Immutable types: int, float, str, tuple, frozenset, bytes. -> the data cannot be changed after it's created
"""

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

print(e.__hash__())

lista = [1, 2, 3]
f = (lista, "ceva")
f[0][1] = 5
# print(f)

g = b'12345'
# print(type(g))
# print(ord(b'a'))

sett = {1, 2, 3, "aa"}
print(sett)

dictio = {
    "cevapi": 3,
    f: 2
}
print(dictio)
