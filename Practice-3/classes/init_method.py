class Person:
  def __init__(self, name, age=18):#using init method to assign values to properties and perform needed operations 
    #one of parameters with default value
    self.name = name #property name will get value of parameter name
    self.age = age
    #init is executed when program is initialized

p1 = Person("Emil")
p2 = Person("Tobias", 25)

print(p1.name, p1.age)
print(p2.name, p2.age)