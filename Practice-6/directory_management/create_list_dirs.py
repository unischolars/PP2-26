from pathlib import Path
import os
p="C:/Users/rozao/Pop/work/Practice-6/directory_management/sample_folder"
Path(p).mkdir()
os.chdir(p)

l = [["./library/genre/classic"], ["./dishes/cuisine/asian", "./dishes/cuisine/european"]]
dish = ["rice.txt", "beef.txt"]

for i in l:
    c=0
    for index, j in enumerate(i):
        Path(j).mkdir(parents=True, exist_ok=True)
        os.chdir(j)
        if len(i) > 1:
            open(dish[c],"w")
            c+=1
        else:
            open("1999.pdf","w")
        os.chdir(p)

for root, dirs, files in os.walk(p):
     print(f"Current folder: {root}")
     for d in dirs:
        print("   Folder:", d)
     for f in files:
        print("   File:", f)