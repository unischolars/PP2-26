import re
s=input()
def ab (s):
    x=re.search(r"ab*",s)
    y=re.findall(r"ab*",s)
    return x,y
print(ab(s))

