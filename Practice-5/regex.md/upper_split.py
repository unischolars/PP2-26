import re

s = input()

def ab(s):
    x = re.findall(r'[A-Z][a-z]*|[a-z]+', s)
    return x

print(ab(s))