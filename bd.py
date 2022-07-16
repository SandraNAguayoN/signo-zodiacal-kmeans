import pymysql

def obtener_conexion():
    return pymysql.connect(host='localhost',
    user = 'root',
    password = '',
    db = 'signos')
    
    

import pandas as pd
import pyodbc 

conn = pymysql.connect(host='localhost',
    user = 'root',
    password = '',
    db = 'signos')
sql_query = pd.read_sql_query('SELECT * FROM signos_zodiacales'
                              ,conn)

df = pd.DataFrame(sql_query)
df.to_csv(r'C:\Users\sandr\exported_data.csv', index = False) 