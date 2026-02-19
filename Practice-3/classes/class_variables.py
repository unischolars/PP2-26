class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Linus", 30)

del p1.age #deleate property

print(p1.name) # access property 



class Person:
  lastname = "" #class property that all objects share

  def __init__(self, name):
    self.name = name #instance property that differ

p1 = Person("Linus")
p2 = Person("Emil")

Person.lastname = "Refsnes" # modifying class property 

print(p1.lastname)
print(p2.lastname)