import sys
import time
import json
import paho.mqtt.client as mqtt
import random
import cv2
import mediapipe as mp
import numpy as np
import time
mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
v=[]
tme=[]
flag=0
tipIds = [4, 8, 12, 16, 20]
y=(np.diff(v)!=0).sum()
video = cv2.VideoCapture(0)
import datetime
hands = mp_hand.Hands(max_num_hands=1)

host="esj44w.messaging.internetofthings.ibmcloud.com"
clntid="d:esj44w:S_ViSION:cnt-1"
usrname="use-token-auth"
password="++wbTOXaFos0rfti&h"
topic="iot-2/evt/sndg/fmt/json"

client = mqtt.Client(clntid)
client.username_pw_set(usrname,password)
client.connect(host, 1883, 60)

while True:
    try:
        tme.append(int(time.perf_counter()))
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        lmList = []
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
               
                    lmList.append([id, cx, cy])

                mp_draw.draw_landmarks(
                    image, hand_landmark,
                    mp_hand.HAND_CONNECTIONS)

        fingers = []
        if len(lmList) != 0:

            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1) 
            else:
                fingers.append(0)  

            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)  
                else:
                    fingers.append(0) 

            total = fingers.count(1)
            
            if y<=5:
                flag=0
                
                if total == 0:
                    v.append(total)
                    print("1")
                    print(y)
                    

                elif total == 5:
                    v.append(total)
                    print("0")
                    print(y)

            if tme[len(tme)-1]-tme[0]>=7:
                v=[]
                y=0
                
                tme=[]
                print("tme=",tme)
                
                
            elif (y>=6):
                x="EMERGENCY"
                
                print(x)
                client.publish(topic, json.dumps({"r":x}))
                time.sleep(30)
                client.publish(topic, json.dumps({"r":"SAFE"}))
                
                
                                
        y=(np.diff(v)!=0).sum()
        print("sent")
    except IOError:
        print("Erroe")
client.loop()
client.disconnect()
