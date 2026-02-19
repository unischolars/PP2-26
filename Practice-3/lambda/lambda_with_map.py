#lambda often used with built in function like map
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers)) 
#map function applies a function to every item in an iterable
print(doubled)