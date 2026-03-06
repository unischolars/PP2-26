import re
s=input()
def ab (s):
    x = re.sub(r"([A-Z])",lambda m : " "+m.group(1),s)
    return x
print(ab(s))
