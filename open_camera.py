# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 14:38:47 2020

@author: AI & ML
"""

import cv2
import numpy as np
import urllib

URL =  "http://25.121.28.3:8080/shot.jpg"

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    
    imgresp = urllib.request.urlopen(URL)
    imgarray = np.array(bytearray(imgresp.read()),dtype=np.uint8)
    img = cv2.imdecode(imgarray,-1)
    img = cv2.resize(img,(800,500))
    
    faces = cascade.detectMultiScale(img)
    
    for x,y,w,h in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),
                      (0,0,255),2)
    cv2.imshow('cam',img)
    
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()








