import re
s=input()
def ab (s):
    x = re.split(r"[A-Z]",s)
    return x
print(ab(s))
