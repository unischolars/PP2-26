phils=["Socrates", "Nietzsche", "Kant", "Plato", "Hume"]
for i,phil in enumerate(phils,start=1):
    print(i,phil)

towns=["Athens", "Rocken", "Konigsberg", "Athens", "Edinburgh"]
for name, town in zip(phils,towns):
    print(name,"lived in",town)
l=[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
print([x**2 if x%2==1 else x*2-1 for x in l])