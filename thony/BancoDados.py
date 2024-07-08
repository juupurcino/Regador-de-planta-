import pyodbc
import time
import requests
import json

proxies = {'https': "http://disrct:etsps2024401@10.224.200.26:8080"}

server = 'CT-C-001YG\SQLEXPRESS'
database = 'Regador'

def InserirBD(sinal):
    server = 'CT-C-001YG\SQLEXPRESS'
    database = 'Regador'
    
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+'; DATABASE='+database+';Trusted_Connection=yes')
    cursor = cnxn.cursor()
    cursor.execute(f"INSERT into planta (umidadeSolo, temperatura, nivelAgua) VALUES ({sinal['Planta1']['UmidadeSolo']}, {sinal['Planta1']['Temperatura']}, {sinal['NivelAgua']})")
    cursor.commit()
    print("Inserido com sucesso!")

def apresentar(sinal):
    
    print(f"Umidade Solo: {sinal[0]}")
    print(f"Temperatura: {sinal[1]}")
    print(f"Nivel agua: {sinal[2]}")

url = "https://iiot-7276b-default-rtdb.firebaseio.com/Regador.json"

valores = [[], [], []]

while True:

    data = json.loads(requests.get(url, proxies=proxies).content)
    
    print(f"Valores dessa joça {data}")

    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+'; DATABASE='+database+';Trusted_Connection=yes')
    cursor = cnxn.cursor()
    cursor.execute(f"SELECT * from planta")
    resultado = cursor.fetchall()
    umidadeSolo = []
    temperatura = []
    nivelAgua = []
    hora = []

    for i in resultado:
        umidadeSolo.append(i[0])
        temperatura.append(i[1]) 
        nivelAgua.append(i[2])
        hora.append(i[3])   

    print("Temperatura:", temperatura)
    print("Umidade:", umidadeSolo)
    print("Nivel agua: ", nivelAgua)
    print("Hora: ", hora)
    
    InserirBD(data)
    time.sleep(60)