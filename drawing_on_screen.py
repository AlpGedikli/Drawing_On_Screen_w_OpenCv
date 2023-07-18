# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 12:21:53 2023

@author: Alp GEDIKLI
"""

import cv2
import numpy as np
from collections import deque # this function provide listing

vid = cv2.VideoCapture(0)



lower_blue = np.array([100,60,60])
upper_blue = np.array([140,255,250]) #these for masking 

blue_points = [deque(maxlen=512)] # we're keeping blue points
green_points = [deque(maxlen=512)]
red_points = [deque(maxlen=512)]
yellow_points = [deque(maxlen=512)]

blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

colors = [(255,00),(0,255,0),(0,0,255),(0,255,255)] # keeping color 
color_index = 0 

drawingWindow = np.zeros((471,636,3))+255 # 255 provide white color
drawingWindow = cv2.rectangle(drawingWindow,(40,1),(140,65),(0,0,0),2)#collor buttons
drawingWindow = cv2.rectangle(drawingWindow,(160,1),(255,65),colors[0],-1) # -1 filling inside the box
drawingWindow = cv2.rectangle(drawingWindow,(275,1),(370,65),colors[1],-1)
drawingWindow = cv2.rectangle(drawingWindow,(390,1),(485,65),colors[2],-1)
drawingWindow = cv2.rectangle(drawingWindow,(505,1),(600,65),colors[3],-1)

font = cv2.FONT_HERSHEY_COMPLEX
cv2.putText(drawingWindow,"All Clear",(49,33),font,0.5,(0,0,0),2,cv2.LINE_AA)
cv2.putText(drawingWindow,"Blue",(185,33),font,0.5,(255,255,255),2,cv2.LINE_AA)
cv2.putText(drawingWindow,"Green",(298,33),font,0.5,(255,255,255),2,cv2.LINE_AA)
cv2.putText(drawingWindow,"Red",(420,33),font,0.5,(255,255,255),2,cv2.LINE_AA)
cv2.putText(drawingWindow,"Yellow",(520,33),font,0.5,(255,255,255),2,cv2.LINE_AA)



cv2.namedWindow("Paint")


while 1:
    ret,frame = vid.read()
    frame= cv2.flip(frame,1)
    
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
   
    frame = cv2.rectangle(frame,(40,1),(140,65),(0,0,0),2)#collor buttons
    frame = cv2.rectangle(frame,(160,1),(255,65),colors[0],-1) # -1 filling inside the box
    frame = cv2.rectangle(frame,(275,1),(370,65),colors[1],-1)
    frame = cv2.rectangle(frame,(390,1),(485,65),colors[2],-1)
    frame = cv2.rectangle(frame,(505,1),(600,65),colors[3],-1)

    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(frame,"All Clear",(49,33),font,0.5,(0,0,0),2,cv2.LINE_AA)
    cv2.putText(frame,"Blue",(185,33),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,"Green",(298,33),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,"Red",(420,33),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame,"Yellow",(520,33),font,0.5,(255,255,255),2,cv2.LINE_AA)
    
    if ret is False:
        break
    
    mask = cv2.inRange(hsv,lower_blue,upper_blue) # we are masking as we said above
    mask = cv2.erode(mask,(5,5),iterations = 2)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,(5,5))
    mask = cv2.dilate(mask,(5,5), iterations = 1)
     
    
    contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    center = None

    if len(contours)>0:
        max_contours = sorted(contours,key = cv2.contourArea,reverse = True)[0]
        ((x,y),radius) = cv2.minEnclosingCircle(max_contours)
        cv2.circle(frame,(int(x),int(y)),int(radius),(255,0,255),3)
    
        M = cv2.moments(max_contours) #center of max contours
        center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"])) # x and y values of center
        
        if center[1] <= 65:
            if 40<=center[0]<=140:

                blue_points = [deque(maxlen=512)]
                green_points = [deque(maxlen=512)]
                red_points = [deque(maxlen=512)]
                yellow_points = [deque(maxlen=512)]

                blue_index=0
                green_index=0
                red_index=0
                yellow_index=0

                drawingWindow[67:,:,:]=255

            elif 160<=center[0]<=255:
                color_index = 0

            elif 275<=center[0]<=370:
                color_index = 1

            elif 390<=center[0]<=485:
                color_index = 2

            elif 505<=center[0]<=600:
                color_index = 3

        else:
            if color_index == 0:
                blue_points[blue_index].appendleft(center)
                
            elif color_index == 1:    
                green_points[green_index].appendleft(center)
                
            elif color_index == 2:
                red_points[red_index].appendleft(center)
                
            elif color_index == 3:
                yellow_points[yellow_index].appendleft(center)

    else:
        blue_points.append(deque(maxlen=512))
        blue_index+=1
        
        green_points.append(deque(maxlen=512))
        green_index+=1
        
        red_points.append(deque(maxlen=512))
        red_index+=1
        
        yellow_points.append(deque(maxlen=512))
        yellow_index+=1

    points = [blue_points,green_points,red_points,yellow_points]
    
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1,len(points[i][j])):
                if points[i][j][k-1] is None or points[i][j][k] is None:
                    continue
                
                cv2.line(frame,points[i][j][k-1], points[i][j][k], colors[i], 2)
                cv2.line(drawingWindow,points[i][j][k-1], points[i][j][k], colors[i], 2)
                

    cv2.imshow("Frame",frame)
    cv2.imshow("Paint",drawingWindow)
    
    if cv2.waitKey(3) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
        
        
    
    
    
    
    
   