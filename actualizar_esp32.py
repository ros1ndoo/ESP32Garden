import os

def actualizar():
    archivo_config = "settup.txt"
    if not os.path.exists(archivo_config):
        print(f"Error: {archivo_config} no encontrado.")
        return

    config = {}
    with open(archivo_config, "r") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                config[k.strip()] = v.strip()

    directorio_destino = "iot_esp32_huerto"
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)

    ruta_h = os.path.join(directorio_destino, "Credenciales.h")
    
    contenido = f"""#ifndef CREDENCIALES_H
#define CREDENCIALES_H

const char* ssid = "{config.get('WIFI_SSID', '')}";
const char* password = "{config.get('WIFI_PASS', '')}";

#endif"""

    with open(ruta_h, "w") as f:
        f.write(contenido)
    
    print(f"Sincronización completada: {ruta_h}")

if __name__ == "__main__":
    actualizar()