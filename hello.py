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