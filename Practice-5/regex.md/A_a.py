import re
s=input()
def ab (s):
    x=re.search(r"[A-Z]{1}[a-z]+",s)
    y=re.findall(r"[A-Z]{1}[a-z]+",s)
    return x,y
print(ab(s))

import re
s=input()
def ab (s):
    pat=re.compile(r"")
    x=pat.search(s)
    y=pat.findall(s)
    return x,y
print(ab(s))
