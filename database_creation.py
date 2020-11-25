# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 14:51:08 2020

@author: AI & ML
"""

import sqlite3 as sql
import io
import numpy as np

con = sql.connect('attendence_sys.db')
con.close()

"""
Student details Table creation
"""
con = sql.connect('attendence_sys.db')

query = """CREATE TABLE student_details(Sid TEXT PRIMARY KEY,
                                        Sname TEXT,
                                        Sclass_id TEXT,
                                        Sphone_no INTEGER,
                                        Spassword TEXT)"""

con.execute(query)
con.commit()
con.close()

"""
configuring database to store arrays
"""
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


"""
creating Student_face_data Table
"""

con = sql.connect('attendence_sys.db',detect_types=sql.PARSE_DECLTYPES)

query = """CREATE TABLE student_face_data(Sid TEXT,
                                        arr array,
                                        FOREIGN KEY (Sid)
                                        REFERENCES student_details(Sid)
                                        ON DELETE CASCADE
                                        ON UPDATE CASCADE)"""
con.execute(query)
con.commit()
con.close()

"""
Student attendence
"""

con = sql.connect('attendence_sys.db',detect_types=sql.PARSE_DECLTYPES)

query = """CREATE TABLE student_attendence(Sid TEXT,
                                        date TEXT,
                                        attendence TEXT DEFAULT 'A',
                                        FOREIGN KEY (Sid)
                                        REFERENCES student_details(Sid)
                                        ON DELETE CASCADE
                                        ON UPDATE CASCADE)"""
con.execute(query)
con.commit()
con.close()





















