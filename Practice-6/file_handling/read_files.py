with open("C:/Users/rozao/Pop/work/Practice-6/file_handling/sample.txt") as f:
   print(f.read())
f=open("C:/Users/rozao/Pop/work/Practice-6/file_handling/sample.txt","r")
for i in f.readlines():
    print(i,end="")
f.close()

