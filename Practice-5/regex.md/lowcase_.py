import re
s=input()
def ab (s):
    x=re.search(r"[a-z]+(?:_[a-z]+)+",s)
    y=re.findall(r"[a-z]+(?:_[a-z]+)+",s)
    return x.group(),y
print(ab(s))
