n=int(input())
m=int(input())
def squ (n):
    for i in range(1,n+1):
        yield i**2
for g in squ(n):
    print(g,end=",")
print()


def evenn(n):
    for i in range(0,n+1,2):
        yield i
for g in evenn(n):
    print(g,end=",")
print()


def threefore(n):
    for i in range(n+1):
        if i%3==0 and i%4==0:
            yield i
for g in threefore(n):
    print(g,end=",")
print()

def ab (a,b):
    for i in range(a,b+1):
        yield i**2
for g in ab(n,m):
    print(g,end=",")
print()

def tozero(n):
    for i in range(n,-1,-1):
        yield i
for g in tozero(n):
    print(g,end=",")




