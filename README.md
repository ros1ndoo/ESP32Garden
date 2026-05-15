# 🌱 ESP32 GARDEN: Monitorización Ambiental en Tiempo Real

Este repositorio contiene la arquitectura completa (hardware y software) de un sistema *Internet of Things* (IoT) diseñado para la monitorización en tiempo real de variables ambientales y de suelo en entornos agrícolas o jardines. 

El proyecto abarca desde la captura de datos físicos mediante sensores y un microcontrolador ESP32, hasta la ingesta de datos, procesamiento y visualización interactiva a través de un dashboard web, todo ello orquestado desde un panel de control gráfico unificado.

## 🛠️ Arquitectura de Hardware

Para replicar este proyecto en el entorno físico, se requieren los siguientes componentes:

* **Microcontrolador:** ESP32 (Módulo con conectividad Wi-Fi integrada).
* **Sensor de Temperatura y Humedad Ambiente:** DHT11.
* **Sensor de Humedad del Suelo:** Sensor capacitivo o resistivo analógico.
* **Sensor de Lluvia / Gotas:** Módulo detector analógico.
* **Carcasa Física:** Estructura protectora diseñada e impresa en 3D para albergar la electrónica de forma segura.

## 💻 Tecnologías y Software

* **Firmware (C++ / Arduino):** Lectura analógica/digital de sensores y servidor web asíncrono para exponer una API REST (formato JSON).
* **Ingesta de Datos (Python):** Peticiones HTTP (`requests`), transformación de datos y almacenamiento histórico mediante `pandas`.
* **Visualización Web (Python):** Aplicación interactiva construida con `streamlit` y visualizaciones gráficas avanzadas con `plotly`.
* **Orquestación (Python):** Interfaz gráfica de usuario (GUI) desarrollada con `tkinter` para la gestión unificada de los microservicios.

## 📂 Estructura del Proyecto

El repositorio está organizado en los siguientes módulos principales:

* `iot_esp32_huerto/`: Directorio que contiene el firmware en C++ (`.ino`) para el microcontrolador ESP32.
* `settup.txt`: Archivo de configuración centralizado (IP del ESP32, SSID y Contraseña de la red Wi-Fi).
* `actualizar_esp32.py`: Script de sincronización que inyecta dinámicamente las credenciales de red desde `settup.txt` hacia el entorno de C++ (generando `Credenciales.h`).
* `main.py`: Panel de Control (Manager) gráfico para administrar los servicios de ingesta y visualización.
* `captura.py`: Servicio en segundo plano que consulta continuamente la API del ESP32 y almacena los registros en `datos_jardin.csv`.
* `dashboard.py`: Aplicación analítica web orientada a la toma de decisiones.
* `requirements.txt`: Dependencias del entorno de Python.

## 🚀 Guía de Instalación y Despliegue

### 1. Despliegue del Hardware (ESP32)
1. Conecta los sensores a los pines correspondientes del ESP32 definidos en el código fuente.
2. Abre el archivo `settup.txt` y configura tu red Wi-Fi (`WIFI_SSID` y `WIFI_PASS`).
3. Ejecuta el archivo `main.py` y haz clic en el botón **"Aplicar"** en la sección de configuración. Esto generará automáticamente el archivo de cabecera seguro (`Credenciales.h`) para el ESP32.
4. Abre el archivo principal `.ino` desde el Arduino IDE y súbelo (Flash) a la placa ESP32. 
5. Una vez conectado, el ESP32 mostrará su dirección IP por el puerto serie. Cópiala y actualiza el campo `IP_ESP32` en el archivo `settup.txt`.

### 2. Despliegue del Entorno de Software
1. Ejecuta el Panel de Control unificado:
   ```bash
   python main.py
