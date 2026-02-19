class Calculator:#methods are just a functions that belongs to class they made it behaviour 
  def add(self, a, b):#make a fuction add 
    return a + b

  def multiply(self, a, b):#make a function multiply 
    return a * b

calc = Calculator()#make an object calc
print(calc.add(5, 3)) #use it add method
print(calc.multiply(4, 7))