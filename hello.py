"""
Ignore the contents of this file, i'm just making some 
tests
"""

print((-1) % 5)
print(ord(' '))
print(ord('A'))

v = list(map(lambda c: ord(c), "AABAAAAAAAAAAAA"))

s = ''.join(list(map(lambda val: chr(val), v)))

print(v)
print(type(s))
print(s)

temp = {
    1 : 2,
    3 : 4,
    5 : 6,
}

# for i in temp:
#     print(temp[i])

text = "ABAABCCACBBC"
# text = "RSTCS JLSLR SLFEL GWLFI ISIKR MGL"

text = ''.join(text.split())
print(text)
n = 4

table = n * [""]

for i in range(len(text)):
    table[i % n] += text[i]

print(table)


exit(0)
alf_list = ['a', 'c', 'd', 'g', 'e', 'z', 'v', 'h', 'f', 'g']

chave = input("Qual a chave? ")
# alf_list.sort()
# print(table)
# print(alf_list)

print(len(chave))
def count(text):
    hist = dict()
    for i in range(26):
        hist[chr(i + 65)] = 0

    hist[' '] = 0
    # print(hist)
    for c in text:
        hist[c] += 1

    return hist