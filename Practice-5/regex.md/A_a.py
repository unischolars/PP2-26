import re
s=input()
def ab (s):
    x=re.search(r"[A-Z]{1}[a-z]+",s)
    y=re.findall(r"[A-Z]{1}[a-z]+",s)
    return x,y
print(ab(s))