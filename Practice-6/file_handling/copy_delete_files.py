from pathlib import Path
import shutil
shutil.copyfile("C:/Users/rozao/Pop/work/Practice-6/file_handling/sample.txt","C:/Users/rozao/Pop/work/Practice-6/file_handling/sample.txt1")
p=Path("C:/Users/rozao/Pop/work/Practice-6/file_handling/sample.txt")
p.unlink()