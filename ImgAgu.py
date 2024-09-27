import cv2
import numpy as np
import random
import glob2
import os
import shutil
import image_augmentation

def colorjitter(img, cj_type):
    if cj_type == "b":
        # value = random.randint(-50, 50)
        value = np.random.choice(np.array([-50, -40, -30, 30, 40, 50]))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        if value >= 0:
            lim = 255 - value
            v[v > lim] = 255
            v[v <= lim] += value
        else:
            lim = np.absolute(value)
            v[v < lim] = 0
            v[v >= lim] -= np.absolute(value)

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    elif cj_type == "s":
        # value = random.randint(-50, 50)
        value = np.random.choice(np.array([-50, -40, -30, 30, 40, 50]))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        if value >= 0:
            lim = 255 - value
            s[s > lim] = 255
            s[s <= lim] += value
        else:
            lim = np.absolute(value)
            s[s < lim] = 0
            s[s >= lim] -= np.absolute(value)

        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    elif cj_type == "c":
        brightness = 10
        contrast = random.randint(40, 100)
        dummy = np.int16(img)
        dummy = dummy * (contrast / 127 + 1) - contrast + brightness
        dummy = np.clip(dummy, 0, 255)
        img = np.uint8(dummy)
        return img

    elif cj_type == "gauss":
        image = img.copy()
        mean = 0
        st = 0.7
        gauss = np.random.normal(mean, st, image.shape)
        gauss = gauss.astype('uint8')
        image = cv2.add(image, gauss)
        return image

    elif cj_type== "sp":
        image = img.copy()
        prob = 0.05
        if len(image.shape) == 2:
            black = 0
            white = 255
        else:
            colorspace = image.shape[2]
            if colorspace == 3:  # RGB
                black = np.array([0, 0, 0], dtype='uint8')
                white = np.array([255, 255, 255], dtype='uint8')
            else:  # RGBA
                black = np.array([0, 0, 0, 255], dtype='uint8')
                white = np.array([255, 255, 255, 255], dtype='uint8')
        probs = np.random.random(image.shape[:2])
        image[probs < (prob / 2)] = black
        image[probs > 1 - (prob / 2)] = white
        return image
    elif cj_type == "blur":
        image = img.copy()
        fsize = 9
        return cv2.blur(image, (fsize, fsize))

    elif cj_type == "gaussian":
        image = img.copy()
        fsize = 9
        return cv2.GaussianBlur(image, (fsize, fsize), 0)

    elif cj_type == "median":
        image = img.copy()
        fsize = 9
        return cv2.medianBlur(image, fsize)





def main():
    print("inside the main")
    f=open('C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\imageAug\\results.txt','r')
    l = f.readline()
    count = 0
    # Iterate directory
    path=l
    print(path)
    for f in os.listdir(path):
        count += 1

    newcount=count+10
    for img_path in os.listdir(path):
        img_path=path+"/"+img_path
        print("img_path = ",img_path)
        img=cv2.imread(img_path)
        d_list=['b','s','c','gauss','sp','blur',"median","gaussian"]
        i=random.choice([0,1,2])
        d=d_list[i]
        img=colorjitter(img,d)
        os.chdir('C:\\Users\\maqwi\\Desktop\\major_project[1]\\major_project\\imageAug')
        file='img'+str(newcount+1)+'.jpg'
        cv2.imwrite(file,img)
        newcount+=1
    newcount=count+100
