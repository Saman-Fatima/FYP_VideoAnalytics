import numpy as np
import cv2
import mysql.connector
import os
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="person_counter"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS heatmap (Sr INT AUTO_INCREMENT PRIMARY KEY,Photo LONGBLOB NOT NULL , timestampp TIMESTAMP)")

# use it if you wonna write video or ffmpeg
# from skvideo.io import FFmpegWriter

start = 1
duration = 10
fps = '30'
cap = cv2.VideoCapture("p1.mp4")
#outfile = 'heatmap.mp4'

for i in range(19):
    print(i, cap.get(i))

w = cap.get(3)
h = cap.get(4)
print('height:',h)
font=cv2.FONT_HERSHEY_SIMPLEX
while True:
    try:
        _, f = cap.read()
        f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        f = cv2.GaussianBlur(f, (11, 11), 2, 2)
        cnt = 0
        res = 0.05 * f
        res = res.astype(np.float64)
        break
    except:
        print('s')

fgbg = cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=100,
                                          detectShadows=True)

# writer = FFmpegWriter(outfile, outputdict={'-r': fps})
# writer = FFmpegWriter(outfile)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
cnt = 0
sec = 0
picc=0;
while True:
    # if sec == duration: break
    cnt += 1
    if cnt % int(fps) == 0:
        #print(sec)
        sec += 1
    ret, frame = cap.read()
    if not ret: break
    fgmask = fgbg.apply(frame, None, 0.01)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # if cnt == 30: res
    gray = cv2.GaussianBlur(gray, (11, 11), 2, 2)
    gray = gray.astype(np.float64)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    fgmask = fgmask.astype(np.float64)
    res += (40 * fgmask + gray) * 0.01
    res_show = res / res.max()
    res_show = np.floor(res_show * 255)
    res_show = res_show.astype(np.uint8)
    res_show = cv2.applyColorMap(res_show, cv2.COLORMAP_JET)

    res_show=cv2.line(res_show,(int(w/3),0),(int(w/3),int(h)),(0,0,255),2) # vertical
    res_show = cv2.line(res_show, (int((2*w)/3), 0), (int((2*w)/3), int(h)), (0, 0, 255), 2)
    res_show = cv2.line(res_show, (0,int(h/3)), (int(w),int(h/3)), (0, 0, 255), 2)  #horizontal
    res_show = cv2.line(res_show, (0, int((2*h)/3)), (int(w),int((2*h)/3) ), (0, 0, 255), 2)
    cv2.putText(res_show, "Nikon", (int((1*w)/9), int((h)/9)), font, 1, (0, 0, 255), 2)# writing  in centre
    cv2.putText(res_show, "Cannon", (int((4 * w) / 9), int((h) / 9)), font, 1, (0, 0, 255), 2)
    cv2.putText(res_show, "Samsung", (int((7 * w) / 9), int((h) / 9)), font, 1, (0, 0, 255), 2)
    cv2.putText(res_show, "Olays", (int((1 * w) / 9), int((4*h) / 9)), font, 1, (0, 0, 255), 2)
    cv2.putText(res_show, "Hersheys", (int((4 * w) / 9), int((4 * h) / 9)), font, 1, (0, 0, 255), 2)
    cv2.putText(res_show, "Panasonic", (int((7 * w) / 9), int((4 * h) / 9)), font, 1, (0, 0, 255), 2)
    cv2.putText(res_show, "Nestle", (int((1 * w) / 9), int((7 * h) / 9)), font, 1, (0, 0, 255), 2)
    cv2.putText(res_show, "Kellogg's", (int((4 * w) / 9), int((7 * h) / 9)),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(res_show, "Coach", (int((7 * w) / 9), int((7 * h) / 9)), font, 1, (0, 0, 255), 2)
    path ='venv\Lib\site-packages\static\people_photo'
    cv2.imshow('Heatmap', res_show)
    if(picc%100==0):

      cv2.imwrite(os.path.join(path,'pico'+str(picc)+'.jpg'),res_show)
      Filepath = "pico"+str(picc)+".jpg"
      with open(Filepath, 'rb') as File:
          BinaryData=File.read()
      query1="INSERT INTO heatmap (Photo) VALUES (%s)"
      mycursor.execute(query1,(BinaryData,))
      mydb.commit()

    picc+=1
    # if sec < start: continue
    #    try:
    #        writer.writeFrame(res_show)
    #    except:
    #        writer.close()
    #        break

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# writer.close()
cap.release()
cv2.destroyAllWindows()