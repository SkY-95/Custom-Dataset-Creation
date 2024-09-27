
from ultralytics import YOLO
import glob

from pathlib import Path
import glob
import os
f=[]
p = Path(r'C:\Users\maqwi\Desktop\major_project[1]\major_project\dataset\train\images')
for i in os.listdir(p):
    f.append(i)
print(f)

