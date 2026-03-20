from pathlib import Path
import shutil
import os
p="C:/Users/rozao/Pop/work/Practice-6/directory_management/sample_folder"
os.chdir(p)
cop=Path("./copydir")
mov=Path("./movedir")
cop.mkdir(exist_ok=True)
mov.mkdir(exist_ok=True)
files = [f for f in Path(p).rglob("*.txt") if f.is_file()]
for f in files:
    shutil.copy(f, Path.joinpath(cop,str(f.name)))
for f in files:
    shutil.move(str(f),  Path.joinpath(mov,str(f.name)))
