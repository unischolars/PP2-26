import re
s=input()
def ab (s):
    x = re.sub(r"_([a-z])",lambda k: k.group(1).upper(),s)
    return x
print(ab(s))
