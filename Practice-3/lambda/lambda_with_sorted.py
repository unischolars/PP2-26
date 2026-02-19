students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
#sort is function that dont change the list but sort it based on "key" argument
print(sorted_students)