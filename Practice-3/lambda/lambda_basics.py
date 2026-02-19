x = lambda a, b, c : a + b + c #lambda is an anonymus functions that can accept endless number of values
#but perform only one expression that they will return
print(x(5, 6, 2))
#they are better for short time usage
def myfunc(n): #they mainly used in other functions
  return lambda a : a * n