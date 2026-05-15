import requests
import pandas as pd
import time
import os
from datetime import datetime

def cargar_ip():
    archivo_config = "settup.txt"
    if os.path.exists(archivo_config):
        with open(archivo_config, "r") as f:
            for line in f:
                if "IP_ESP32" in line:
                    return line.strip().split("=")[1].strip()
    return "192.168.0.110"

IP_ESP32 = cargar_ip()
URL = f"http://{IP_ESP32}/json"
CSV = "datos_jardin.csv"
COLUMNAS = ['fecha_hora', 'temperatura', 'humedad_amb', 'suelo', 'lluvia']

while True:
    try:
        r = requests.get(URL, timeout=5)
        raw = r.json()
        
        nueva_fila = {
            'fecha_hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'temperatura': raw.get('temperatura', 0),
            'humedad_amb': raw.get('humedad_amb', 0),
            'suelo': raw.get('suelo', 0),
            'lluvia': raw.get('lluvia', 0)
        }
        
        df = pd.DataFrame([nueva_fila])
        
        if not os.path.exists(CSV):
            df.to_csv(CSV, index=False, columns=COLUMNAS)
        else:
            df.to_csv(CSV, mode='a', header=False, index=False, columns=COLUMNAS)
            
        print(f"[{nueva_fila['fecha_hora']}] Registro almacenado: {nueva_fila['temperatura']}°C")
        
    except Exception as e:
        print(f"Error de red: {e}")
    
    time.sleep(5)