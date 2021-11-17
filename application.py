import ibmiotf.application
import time
import json
option= {
    "org":"esj44w",
    "id":"app1",
    "auth-method":"apikey",
    "auth-key":"a-esj44w-fwzkpxkpjz",
    "auth-token":"rAoFIswqElQzLW-Dwe",
    "clean-session":True
    }

sourceDeviceType="Dashcom"
sourceDeviceId="com-1"
sourceEvent="sndg1"
targetDeviceType="S_ViSION"
targetDeviceId="cnt-1"

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
clntid="d:esj44w:Dashcom:com-1"
usrname="use-token-auth"
password="53+CUj!v0nWpIX4oai"
topic="iot-2/evt/sndg1/fmt/json"

client1= mqtt.Client(clntid)
client1.username_pw_set(usrname,password)
client1.connect(host, 1883, 60)

def publs():


                try:
                        payload={"r":"ATTENDEE SENT"}
                        client1.publish(topic, json.dumps(payload))
                        print("SENT")
                        time.sleep(2)

                except IOError:
                        print("Error")

                         

publs()

def ButtonCallback(event):
    print("Got event" + json.dumps(event.data))
    button=event.data["r"]
    print(button)
    commandData={"state":button}
    client.publishCommand(targetDeviceType,targetDeviceId,"state","json",commandData)


client = ibmiotf.application.Client(option)
client.connect()
client.deviceEventCallback = ButtonCallback
client.subscribeToDeviceEvents(deviceType=sourceDeviceType,deviceId=sourceDeviceId,event=sourceEvent)

