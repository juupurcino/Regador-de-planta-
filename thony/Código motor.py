from machine import Pin, ADC
import time
import dht
import network
import ujson
import urequests

#Definição dos pinos
sinalUmi = ADC(Pin(34))
dht_sensor = dht.DHT11(Pin(25))
base = Pin(33, Pin.OUT)
nivel_agua = Pin(23, Pin.IN)
regar = 0

#Credenciais do wifi
nome = "Wifi Amilton"
senha = "87654321"

# Endereço do firebase
FIREBASE_URL = "https://iiot-7276b-default-rtdb.firebaseio.com/"
SECRET_KEY = ""


def conectarWifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando no WiFi...")
        wlan.connect(nome, senha)
        while not wlan.isconnected():
            pass
    print("Wifi conectado... IP: {}".format(wlan.ifconfig()[0]))


conectarWifi()

def read_dht11():
    global temp, hum
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        print("\n------ SENSOR DHT11 ------")
        print(f"| Temperatura: {temp}°C     | \n| Umidade: {hum}%           |")
        print("--------------------------")
    except OSError as e:
        print("Falha na leitura do sensor:", e)

def ler_umi():
    sinalUmi.atten(ADC.ATTN_11DB)
    value = round(sinalUmi.read() * 100 / 4095)
    value = 100 - value 
    return value

def enviar_para_firebase(data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + SECRET_KEY
    }
    url = FIREBASE_URL + "Regador.json"

    try:
        response = urequests.put(url, data=ujson.dumps(data), headers=headers)
        print("\nResposta do Firebase:", response.text)
        response.close()
    except Exception as e:
        print("Erro ao enviar para o Firebase:", e)
        
def receberFire():
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + SECRET_KEY
    }
    
    # Endereço do firebase
    url = "https://iiot-7276b-default-rtdb.firebaseio.com/Regador.json"
    response = urequests.get(url, headers=headers)
    qualquer = ujson.loads(response.text)
    response.close()
    return qualquer

while True:
    
    read_dht11()
    
    print(f"\n-------------")
    print("|CLICA AGORA|")
    print(f"-------------")
    time.sleep(3)
    fireBase = receberFire()
    regar = fireBase["Repor"]

    # Leitura do sensor de umidade do solo
    value = ler_umi()
    agua = nivel_agua.value()
    
    print(f"\n------------------------")
    print(f"| Umidade do solo: {value}  |")
    print(f"| Nível de água: {agua}     |")
    print(f"------------------------")
    
    # Controle da base
    if value <= 10 or regar == 1:
        base.on()
        print("---------------")
        print("| BASE LIGADA |")
        print("---------------")
        time.sleep(3)
        base.off()
        regar = 0
    else:
        base.off()
        print("------------------")
        print("| BASE DESLIGADA |")
        print("------------------")
        
        
    # Montagem dos dados para envio ao Firebase
    informacao = {
        
        "Planta1": {
            "Temperatura": temp,
            "UmidadeSolo": value,
        },
        
        "NivelAgua" : agua,
        "Repor" : regar,
    }
    
    # Envio para o Firebase
    enviar_para_firebase(informacao)

    time.sleep(0.5)