import numpy as np
import cv2
import os
import math
import json
from StringIO import StringIO
cap=cv2.VideoCapture(0)
while 1:
    ret,img=cap.read()
    #img = cv2.imread(file)
    #img= cv2.imread("105.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret,thresh = cv2.threshold(gray,127,255,1)

    contours,h = cv2.findContours(thresh,1,2)
    sign_list=[]
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        area=cv2.contourArea(cnt);
        if len(approx)==8 and area>2000 and cv2.contourArea(cv2.convexHull(cnt))/area<1.1:
            distance= 10000/math.sqrt(area)
            print "STOP distance"+ str(distance)
            sign_list.append( ("STOP",distance))
            cv2.drawContours(img,[cnt],0,(255,255,0),3)
    io = StringIO()
    json.dump(sign_list, io)
    
    cv2.imshow('img',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
