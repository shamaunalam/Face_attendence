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
from datetime import timedelta,datetime


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
        
        con = sql.connect('attendence_sys.db',detect_types=sql.PARSE_DECLTYPES)
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        query = """INSERT INTO student_details(Sid,
                                                Sname,
                                                Sclass_id,
                                                Sphone_no,
                                                Spassword) values(?,?,?,?,?)"""
        con.execute(query,(Sid,Sname,Sclass_id,Sphone_no,Spassword))
        
        query = """INSERT INTO student_face_data(Sid,arr) VALUES(?,?)"""
        
        con.execute(query,(Sid,emb))
        
        con.commit()
        con.close()
        
    def fetch_student(self,Sphone_no,Spassword):
            cur = sql.connect('attendence_sys.db',detect_types=sql.PARSE_DECLTYPES)
            query = """SELECT * FROM student_details WHERE Sphone_no=? AND Spassword=?"""
            
            ret = cur.execute(query,(Sphone_no,Spassword))
            try:
                
                ret = ret.fetchall()[0]
                
                if len(ret)>0:
                    return {'Sid':ret[0],'Sname':ret[1],'Sclass':ret[2],
                            'Sphone':ret[3]}
                else:
                    return False
                cur.close()
            except:
                return False
            
    
    def fetch_student_attendence(self,Sid,startdate,enddate):
        con = sql.connect('attendence_sys.db',detect_types=sql.PARSE_DECLTYPES)
        ret = con.execute("""SELECT Sname FROM student_details WHERE Sid=?""",(Sid,))
        ret=ret.fetchall()
        if len(ret)>0:
            atten = {"Roll":[Sid],"Name":[ret[0][0]]}
            
        daterange = []
        start = datetime.strptime(startdate,"%d-%m-%y")
        end = datetime.strptime(enddate,"%d-%m-%y")
        step = timedelta(days=1)
        while start<=end:
            daterange.append(start.strftime("%d-%m-%y"))
            start = start + step
        for i in daterange:
            query = """SELECT Sid FROM student_attendence WHERE date=?"""
            ret = con.execute(query,(i,))
            ret = ret.fetchall()
            ret = [x[0] for x in ret]
            if Sid in ret:
                atten.update({i:["P"]})
            else:
                atten.update({i:["A"]})
        con.close()
        return atten


class Employee:
    
    def register_faculty(self,Eid,Ename,Ephone,Epassword,Etype):
        
        con = sql.connect('attendence_sys.db',detect_types=sql.PARSE_DECLTYPES)

        query = """INSERT INTO employee_details(Eid,
                                                Ename,
                                                Ephone,
                                                Epassword,
                                                Etype) VALUES (?,?,?,?,?)"""
        con.execute(query,(Eid,Ename,Ephone,Epassword,Etype))
        con.commit()
        con.close()
        
    def fetch_faculty(self,Ephone,Epassword):
        con = sql.connect('attendence_sys.db',detect_types=sql.PARSE_DECLTYPES)

        query = """SELECT * FROM employee_details WHERE Ephone=? AND Epassword=?"""
        ret = con.execute(query,(Ephone,Epassword))
        ret = ret.fetchall()
        if len(ret)>0:
            return {'Eid':ret[0][0],'Ename':ret[0][1],'Enumber':ret[0][2],'Etype':ret[0][4]}
        else:
            return False
        con.close()


