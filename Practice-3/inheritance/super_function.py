class Person: #parent class with properties and method that will be inherited
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)


class Student(Person):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year
#super function will automaticly make child class inherit all methods and properties from parent

x = Student("Mike", "Olsen", 2019)