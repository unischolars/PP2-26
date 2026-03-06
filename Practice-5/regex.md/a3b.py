import re
s=input()
def ab (s):
    x=re.search(r"ab{2,3}",s)
    y=re.findall(r"ab{2,3}",s)
    return x,y
print(ab(s))

