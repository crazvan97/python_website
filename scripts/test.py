def pass_by_reference(cevapi):
    cevapi.append("F")
    print(cevapi)


cevapi = ["A", "B"]
pass_by_reference(cevapi)


# a = {1, 2, 3, ["cevap"]}
# print(a)

# a = ["a"]
# print(hash(a))
# print(id(a))

