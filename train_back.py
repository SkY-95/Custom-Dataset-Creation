import os
import shutil
import time
import yaml
from ultralytics import YOLO
import numpy as np
import glob
import cv2
from pathlib import Path
import re
from ultralytics.data.utils import compress_one_image
from ultralytics.utils.downloads import zip_directory
def main():

    f = open("C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\train\\results.txt", "r")
    lines = f.readlines()
    f.close()
    c=0

    if len(os.listdir("C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\dataset\\train\\images"))!=0:
        files=glob.glob("C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\dataset\\train\\images")
        for f in files:
            os.remove(f)
    if len(os.listdir("C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\dataset\\train\\labels"))!=0:
        files=glob.glob("C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\dataset\\train\\labels")
        for f in files:
            os.remove(f)

    src_m="C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\dataset\\images\\train"
    src_l="C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\dataset\\labels\\train"

    classes=[]
    names=[]

    for i in lines:
        pt=0
        i = i.replace('\n', '')
        p=i+"\\labels"
        for point in range(len(i)-1,0,-1):
            if i[point]=="/":
                pt=point+1
                break
        names.append(i[pt:])
        for i in os.listdir(p):
            p=p+"\\"+i
            f=open(p,"r")
            for j in f:
                classes.append(j[0])
                break
            break


    classfile=open("C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\dataset\\train\\labels\\classes.txt","w")
    classfile.writelines("\n"*100)
    classfile.close()

    for i in range(0,len(classes)):
        classfile = open("C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\dataset\\train\\labels\\classes.txt", "r")
        a=classfile.readlines()

        a[int(classes[int(i)])]=names[i]+"\n"
        classfile.close()
        classfile = open("C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\dataset\\train\\labels\\classes.txt", "w")
        classfile.writelines(a)
        classfile.close()

    classfile.close()
    yml_name=str(names)
    yml_name=re.sub("['']","",yml_name)
    s=''
    for i in names:
        s=s+i+','

    data={
        'path' :r'C:\Users\maqwi\Desktop\major_project[1]\major_project\dataset',
        'train':r'train\images\\',
        'val' :r"val\images\\",
        'nc': len(classes),
        'names':names
    }
    with open('C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\data.yaml', 'w') as file:

        yaml.dump(data, file)

    for i in lines:

        i=i.replace('\n', '')
        image_path=i+"\\images"
        lable_path=i+"\\labels"
        imagelist=os.listdir(image_path)
        for j in imagelist:

            count = j.split("image", 1)[1]
            delimiter = "."
            s = count.split(delimiter)
            s = s[0]
            p=image_path+"\\image"+s+'.jpg'
            l=lable_path+"\\image"+s+".txt"
            new_image_name=image_path+"\\"+"image_"+str(c)+".jpg"
            new_label_name=lable_path+"\\"+"image_"+str(c)+".txt"
            shutil.move(p,new_image_name)
            shutil.move(l,new_label_name)
            c+=1

    for i in lines:
        i = i.replace('\n', '')
        a=i+"\\images\\"
        b=i+"\\labels\\"
        for j in os.listdir(a):
            new_path_a = r"C:\Users\maqwi\Desktop\major_project[1]\major_project\dataset\train\images" + "\\"+j
            new_lable_path=r"C:\Users\maqwi\Desktop\major_project[1]\major_project\dataset\val\images" + "\\"+j
            shutil.copy(a+j,new_path_a)
            shutil.copy(a + j, new_lable_path)
        for k in os.listdir(b):
            new_path_b = r"C:\Users\maqwi\Desktop\major_project[1]\major_project\dataset\train\labels"+"\\"+k
            new_lable_path_b=r"C:\Users\maqwi\Desktop\major_project[1]\major_project\dataset\val\labels"+"\\"+k
            shutil.copy(b+k,new_path_b)
            shutil.copy(b+k,new_lable_path_b)
    for x in classes:
        for i in os.listdir(r"C:\Users\maqwi\Desktop\major_project[1]\major_project\dataset\train\images"):
            f=open(r"C:\Users\maqwi\Desktop\major_project[1]\major_project\dataset\train\labels.txt","w")

            f.write("train/images/"+i+" "+x+"\n")

    path=Path(r"C:\Users\maqwi\Desktop\major_project[1]\major_project\dataset")
    # Optimize images in dataset (optional)
    for f in path.rglob("*.jpg"):
        compress_one_image(f)

    # Zip dataset into 'path/to/dataset.zip'
    zip_directory(path)

    print("main done")
def run():
    model = YOLO('yolov8n.pt')
    count=len(os.listdir(r"C:\Users\maqwi\Desktop\major_project[1]\major_project\dataset\train\images"))
    print(count)
    model.train(data="C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\data.yaml",epochs=(count-10))



