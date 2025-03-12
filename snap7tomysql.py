import snap7
from snap7.util import get_dint
import mysql.connector

config = {
    "host": "192.168.0.232",     
    "port": 3306,            
    "user": "root",    
    "password": "x",  
    "database": "pruebas" 
}

def InsertarDB(data):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        for valor in data:
            cursor.execute("INSERT INTO monitoreo (valor) VALUES (%s)", (valor,))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error  as e:
        print(f"Error en DB: {e}")
        exit()

def LeerPLC():
    plc = snap7.client.Client()
    plc.connect("192.168.0.150", 0, 1)
  
    db_number = 4
    start = 0
    DBsize = 0
    offset = [0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80]
    for i in range(len(offset)-1):
        resta = offset[i+1] - offset[i]
        DBsize += resta
    data = plc.db_read(db_number, start, DBsize)
    datos = [];
    for i in range(len(offset)-1):
        datos.append( get_dint( data, offset[i] ) )
    plc.disconnect()
    return datos

def Modifica(data):
    return [pow(d, 2) for d in datos];
   
datos = LeerPLC()
datos = Modifica(datos)
InsertarDB(datos)
