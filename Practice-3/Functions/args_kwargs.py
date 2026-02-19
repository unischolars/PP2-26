def my_function(greeting, *names):# * makes args that allow us to save any positional arguments
  for name in names:
    print(greeting, name)

my_function("Hello", "Emil", "Tobias", "Linus")
#args saves values as an tuple

def my_function(**myvar):# ** makes a kwargs that allow us to save any keyword arguments
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

my_function(name = "Tobias", age = 30, city = "Bergen")
#kwarg saves values as an dict 