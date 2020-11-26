# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:52:25 2020

@author: AI & ML
"""

import sqlite3 as sql
import cv2
import numpy as np
from numpy import asarray
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
import io
import urllib

model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
face_data = "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(face_data)
URL =  "http://10.32.63.141:8080/shot.jpg"

def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sql.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

sql.register_adapter(np.ndarray, adapt_array)
sql.register_converter("array", convert_array)


class Student:
    
    
    def preprocess(self,img):
        
        """helper function to preprocess image"""
        
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img = cv2.resize(img,(224,224))
        img = img.reshape(1,224,224,3)
        img = asarray(img,np.float32)
        img = preprocess_input(img,version=2)
        return img
    
    
    
    def register(self,URL,Sid,Sname,Sclass_id,Sphone_no,Spassword):
        
        while True:
    
            imgresp = urllib.request.urlopen(URL)
            imgarray = np.array(bytearray(imgresp.read()),dtype=np.uint8)
            img = cv2.imdecode(imgarray,-1)
            img = cv2.resize(img,(800,500))
            
            faces = cascade.detectMultiScale(img)
            
            for x,y,w,h in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),
                              (0,0,255),2)
                cv2.putText(img,'press q to capture',(10,470),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                face_img = img[y:y+h,x:x+w]
            cv2.imshow('cam',img)
            
            if cv2.waitKey(1)==ord('q'):
                break
        cv2.destroyAllWindows()
        
        emb = model.predict(self.preprocess(face_img))
        
        cur = sql.connect('attendence_sys.db',detect_types=sql.PARSE_DECLTYPES)
        query = """INSERT INTO student_details(Sid,
                                                Sname,
                                                Sclass_id,
                                                Sphone_no,
                                                Spassword) values(?,?,?,?,?)"""
        cur.execute(query,(Sid,Sname,Sclass_id,Sphone_no,Spassword))
        
        query = """INSERT INTO student_face_data(Sid,arr) VALUES(?,?)"""
        
        cur.execute(query,(Sid,emb))
        
        cur.commit()
        cur.close()


