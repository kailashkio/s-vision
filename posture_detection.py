#!/usr/bin/env python3
import cv2
import mediapipe as mp
import argparse
import logging
import time
from pprint import pprint
import cv2
import numpy as np
import sys
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import os


mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--camera', type=str, default=0)
    parser.add_argument('--resize', type=str, default='0x0',
                        help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')

    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    parser.add_argument('--save_video',type=bool,default=False, 
                        help='To write output video. default name file_name_output.avi')
    args = parser.parse_args()
    
    
    
    logger.debug('initialization %s : %s' % (args.model, get_graph_path(args.model)))
    w, h = model_wh(args.resize)
    if w > 0 and h > 0:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368))
    logger.debug('cam read+')
    cam = cv2.VideoCapture(0)
    count=0
    if(args.camera == '0'):
        file_write_name = 'camera_0'
    else:
        pass
        
    ret_val, image = cam.read()
    logger.info('cam image=%dx%d' % (image.shape[1], image.shape[0]))
    count = 0
    y1 = [0,0]
    frame = 0

    tipIds = [4, 8, 12, 16, 20]



    hands = mp_hand.Hands(max_num_hands=1)

while True:
    ret_val, image = cam.read()
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
    i =1
    count+=1
    if count % 11 == 0:
        continue
        
    if not ret_val:
        break
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
        
    image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

    fingers = []
    for human in humans:
        for i in range(len(humans)):
            try:
                a = human.body_parts[0]   
                x = a.x*image.shape[1]
                y = a.y*image.shape[0]   
                y1.append(y)   
            except:
                pass

            if ((y - y1[-2]) > 25):  
                cv2.putText(image, "Fall Detected", (20,50), cv2.FONT_HERSHEY_COMPLEX, 2.5, (0,0,255), 
                        2, 11)
                print("Fall detected",i+1, count)
        
      
        
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
        
       


        if total == 5:
            count=count+1
            """print(count)"""
            if count>100:
                print("Emergency help")
                cv2.putText(image, "Emergency help", (45, 375),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    if count>150:
        count=0
             


    
  
    imS = cv2.resize(image, (960, 720))                   
    cv2.imshow("Patient Detection", imS)     

  

    k = cv2.waitKey(1)
    
    if k == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
