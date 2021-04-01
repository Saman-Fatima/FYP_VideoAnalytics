import cv2
import os
import time
import datetime
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="person_counter"
)

mycursorG = mydb.cursor()

mycursorG.execute("CREATE TABLE IF NOT EXISTS genderData (Sr INT AUTO_INCREMENT PRIMARY KEY,male INT,female INT, timestampp TIMESTAMP)")

data_path='Datasets'
categories=os.listdir(data_path)
labels=[i for i in range(len(categories))]

label_dict=dict(zip(categories,labels))

print(label_dict)
print(categories)
print(labels)
from cv2 import CascadeClassifier

img_size = 32
data = []
target = []

# facedata = "haarcascade_frontalface_default.xml"
# cascade = cv2.CascadeClassifier(facedata)
cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

for category in categories:
    folder_path = os.path.join(data_path, category)
    img_names = os.listdir(folder_path)

    for img_name in img_names:
        img_path = os.path.join(folder_path, img_name)
        img = cv2.imread(img_path)
        faces = cascade.detectMultiScale(img)
        try:
            for f in faces:
                x, y, w, h = [v for v in f]
                sub_face = img[y:y + h, x:x + w]
                gray = cv2.cvtColor(sub_face, cv2.COLOR_BGR2GRAY)
                resized = cv2.resize(gray, (img_size, img_size))
                data.append(resized)
                target.append(label_dict[category])
        except Exception as e:
            print('Exception:', e)

#import tensorflow as tf
#from tensorflow import keras
from keras.models import load_model
import cv2
import numpy as np
model = load_model('./training/model-017.model')
m=0
f=0
face_clsfr=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap=cv2.VideoCapture(0)
for i in range(19):
    print(i, cap.get(i))

w = cap.get(3)
h = cap.get(4)

h_threshold=int(h/2)
w_total=int(w)
print(w_total)
labels_dict={0:'Female',1:'Male'}
color_dict={0:(0,0,255),1:(0,255,0)}
while (True):

    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_clsfr.detectMultiScale(gray, 1.3, 3)

    for (x, y, w, h) in faces:
        face_img = gray[y:y + w, x:x + w]
        resized = cv2.resize(face_img, (32, 32))
        normalized = resized / 255.0
        reshaped = np.reshape(normalized, (1, 32, 32, 1))
        result = model.predict(reshaped)
        #print(x,y,w,h)
        label = np.argmax(result, axis=1)[0]
        cv2.line(img, (0, h_threshold), (w_total, h_threshold), (255, 0, 0), 3) # horizontal line y=same, top(x,y), endPoint(x,y)

        if(y>=h_threshold and y<=(h_threshold+10)):
            cv2.rectangle(img, (x, y), (x + w, y + h), color_dict[label], 2)
            cv2.rectangle(img, (x, y - 40), (x + w, y), color_dict[label], -1)
            print(labels_dict[label])
            print(x, y, w, h)
            if(labels_dict[label]=='Female'):
                f+=1
                sql = "INSERT INTO genderData (male,female,timestampp) VALUES (%s,%s,%s)"
                val = (m,f, datetime.datetime.now())
                mycursorG.execute(sql, val)
            else:
                f += 1
                sql = "INSERT INTO genderData (male,female,timestampp) VALUES (%s,%s,%s)"
                val = (m,f, datetime.datetime.now())
                mycursorG.execute(sql, val)
            mydb.commit()
            cv2.putText(img, labels_dict[label], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow('Result', img)
    k = cv2.waitKey(1)

    if k == ord("q"):
        break

cv2.destroyAllWindows()
cap.release()