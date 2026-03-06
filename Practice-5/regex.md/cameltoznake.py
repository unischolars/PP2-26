import re
s=input()
def ab (s):
    x = re.sub(r"([A-Z])",lambda k: "_"+k.group(1).lower(),s)
    return x
print(ab(s))
