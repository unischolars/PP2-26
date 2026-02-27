import math
x=int(input())
def rad(x):
    return x/180*math.pi
print("in radian:",rad(x))

h=int(input())
b1=int(input())
b2=int(input())
def trap(x,y,z):
    return x*0.5*(y+z)
print("trapezoid area:",trap(h,b1,b2))

n=int(input())
len=float(input())
def pol(n,l):
    return (n*pow(l,2))/(4*math.tan(math.pi/n))
print("area of poligon:",pol(n,len))


hei=float(input())
b=float(input())
def par (h,b):
    return h*b
print("area of parallelogram:",par(hei,b))