from functools import reduce
l=[1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
def flip(x):
    return x+1
def prime(x):
    if x < 2:
        return False
    for i in range(2, int(x ** 0.5) + 1):
        if x % i == 0:
            return False
    return True
m=list(map(flip,l))
f=list(filter(prime,l))
print(reduce(lambda x,y:y-abs(x)*2,m))
print(reduce(lambda x,y:x*y,f)+1)