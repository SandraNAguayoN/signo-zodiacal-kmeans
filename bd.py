import pymysql
import pandas as pd
import pyodbc 
from os import remove

def obtener_conexion():
    return pymysql.connect(host='localhost',
    user = 'root',
    password = '',
    db = 'signos')

#Vuelve a generar el csv para que este actualizado con la BD
conn = pymysql.connect(host='localhost',
    user = 'root',
    password = '',
    db = 'signos')
sql_query = pd.read_sql_query('SELECT * FROM signos_zodiacales'
                              ,conn)

df = pd.DataFrame(sql_query)
remove(r'static\data\exported_data.csv')
remove(r'static\data\exported_data.xlsx')
df.to_csv(r'static\data\exported_data.csv', index = False) 
df.to_excel(r'static\data\exported_data.xlsx', index=False)