import re
s=input()
def ab (s):
    x = re.sub(r"[ ,.]",":",s)
    return x
print(ab(s))
