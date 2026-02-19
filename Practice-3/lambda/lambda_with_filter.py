numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
#filter function creates a list of items for whiches fucntion return true
print(odd_numbers)