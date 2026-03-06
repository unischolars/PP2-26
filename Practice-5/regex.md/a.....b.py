import re
s=input()
def ab (s):
    pat=re.compile(r"^ab.*$")
    x=pat.search(s)
    y=pat.findall(s)
    return x,y
print(ab(s))
