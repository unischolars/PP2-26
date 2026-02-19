class Person: #parent class with properties and method that will be inherited
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)
    
class Student(Person):
  def __init__(self, fname, lname): 
    #when we use the __init__ function it overrides the inheritences
    #meaning that child class no longer inherit its parents __init__ fucntion
    Person.__init__(self, fname, lname)
    #to keep the inheritance we need to call the parent init funciot
