class Person: #parent class with properties and method that will be inherited
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()
class Student(Person): #child class that inherit parameters and methods
  pass
x = Student("Mike", "Olsen")
x.printname()