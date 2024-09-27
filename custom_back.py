from ultralytics import YOLO
import glob
import os
import shutil
import custom
# Load your model
model = YOLO('yolov8n.pt')
from os import listdir
from os.path import isfile, join

# Run inference
def main():
    c=0
    l=os.listdir("C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\customtest")
    for i in l:
        if os.path.isdir(i):
            c+=1
    if os.path.exists('C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\customtest\\lable_value.txt'):
        os.remove('C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\customtest\\lable_value.txt')
        f=open('C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\customtest\\lable_value.txt','w')
        f.write(str(c))
        f.close()


    img_list=[]
    folder_names=[]
    f=open("C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\customtest\\results.txt","r")
    lines= f.readlines()
    for i in lines:
        n=0
        for j in range(len(i)-1,0,-1):
            if i[j]=="/":
                break
            else:
                n=j
        folder_names.append(i[n:len(i)])



    for i in folder_names:

        path="C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\customtest\\"
        i_path=path+i
        i_path = i_path.replace('\n', '')

        if not os.path.exists(i_path):
            os.makedirs(i_path)
        folder_path=i_path+"\\images"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        lable_path=i_path+"\\labels"
        if not os.path.exists(lable_path):
            os.makedirs(lable_path)

    for i in range(len(folder_names)):
        v1=open("C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\customtest\\lable_value.txt","r")
        v2=v1.read()

        lable_id=v2
        print("\n\n\n\n\nv2\n\n\n\n ===",v2)
        v3=int(v2)
        v4=v3+1
        v1.close()
        os.remove("C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\customtest\\lable_value.txt")
        _F_=open("C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\customtest\\lable_value.txt","w")
        _F_.write(str(v4))
        _F_.close()
        lines[i] = lines[i].replace('\n', '')
        folder_names[i]=folder_names[i].replace('\n','')


        for path in os.listdir(lines[i]):
            # check if current path is a file
            if os.path.isfile(os.path.join(lines[i], path)):
                p=lines[i]+"\\"+path
                img_list.append(p)

        for img_path in img_list:

            try:
                results = model.predict(img_path)
            except:
                continue

            result = results[0]
            box = result.boxes[0]
            cords = box.xyxy[0].tolist()
            cords = [round(x) for x in cords]
            class_id = result.names[box.cls[0].item()]
            xmin = cords[0]
            ymin = cords[1]
            w = cords[2]
            h = cords[3]
            w_img=480
            h_img=640

            xcenter = (xmin + w/2) / w_img
            ycenter = (ymin + h/2) / h_img
            w = w / w_img
            h = h / h_img

            count=img_path.split("image",1)[1]


            delimiter="."
            s=count.split(delimiter)
            s=s[0]


            filepath="C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\customtest\\"+folder_names[i]+"\\labels"+"\\"+'image'+s+'.txt'
            dest="C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\customtest\\"+folder_names[i]+"\\images"
            shutil.copy2(img_path,dest)
            text_file = open(filepath, "w")

            text_file.write(str(lable_id)+" ")
            text_file.write(str(ycenter)+" ")
            text_file.write(str(ycenter)+" ")
            text_file.write(str(w)+" ")
            text_file.write(str(h))
            text_file.close()

