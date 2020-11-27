# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 17:13:49 2020

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
from scipy.spatial.distance import cosine

model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
face_data = "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(face_data)
URL =  "http://100.64.206.50:8080/shot.jpg"

def preprocess(img):
        
    """helper function to preprocess image"""
        
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = cv2.resize(img,(224,224))
    img = img.reshape(1,224,224,3)
    img = asarray(img,np.float32)
    img = preprocess_input(img,version=2)
    return img

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


con = sql.connect('attendence_sys.db',detect_types=sql.PARSE_DECLTYPES)

query = """SELECT * FROM student_face_data"""

ret = con.execute(query)

ret = ret.fetchall()

con.close()


def getname(Sid):
    con = sql.connect('attendence_sys.db',detect_types=sql.PARSE_DECLTYPES)
    
    query = """SELECT Sname FROM student_details WHERE Sid=?"""
    
    res = con.execute(query,(Sid,))
    
    res = res.fetchall()[0]
    
    con.close()
    
    return res[0]

while True:
    
    imgresp = urllib.request.urlopen(URL)
    imgarray = np.array(bytearray(imgresp.read()),dtype=np.uint8)
    img = cv2.imdecode(imgarray,-1)
    img = cv2.resize(img,(800,500))
            
    faces = cascade.detectMultiScale(img)
            
    for x,y,w,h in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),
                              (0,0,255),2)
        face_img = img[y:y+h,x:x+w]
        
        new_emb = model.predict(preprocess(face_img))
        
        for i in ret:
            
            if cosine(new_emb,i[1])<0.2:
        
                cv2.putText(img,getname(i[0]),(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                
    cv2.imshow('cam',img)
            
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()



