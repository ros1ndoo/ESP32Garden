import tkinter as tk
import subprocess
import requests
import threading
import sys
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "settup.txt")

def cargar_config():
    config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            for linea in f:
                if "=" in linea:
                    clave, valor = linea.strip().split("=", 1)
                    config[clave.strip()] = valor.strip()
    return config

class PanelControl(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Manager IoT")
        self.geometry("400x350")
        self.configure(padx=20, pady=20, bg="#f4f4f4")
        self.resizable(False, False)

        self.proceso_logger = None
        self.proceso_dashboard = None
        self.config = cargar_config()
        self.ip_esp = self.config.get("IP_ESP32", "127.0.0.1")

        # --- ESTADO ESP32 ---
        self.marco_esp = tk.Frame(self, bg="#f4f4f4")
        self.marco_esp.pack(fill="x", pady=10)
        
        # Guardamos la etiqueta de la IP en una variable para poder actualizarla luego
        self.lbl_ip = tk.Label(self.marco_esp, text=f"ESP32 ({self.ip_esp}):", font=("Arial", 9, "bold"), bg="#f4f4f4")
        self.lbl_ip.pack(side="left")
        
        self.lbl_status = tk.Label(self.marco_esp, text="BUSCANDO...", fg="orange", bg="#f4f4f4")
        self.lbl_status.pack(side="right")

        tk.Frame(self, height=2, bd=1, relief="sunken").pack(fill="x", pady=10)

        # --- BOTONES DE SERVICIOS ---
        self.btn_captura = self.crear_fila("Servicio Captura", self.toggle_captura)
        self.btn_web = self.crear_fila("Dashboard Web", self.toggle_web)
        
        tk.Button(self, text="Instalar requirements.txt", bg="#2196F3", fg="white", 
                  command=self.instalar_req, relief="flat").pack(fill="x", pady=10)
        
        # --- ZONA DE CONFIGURACIÓN (BOTONES LADO A LADO) ---
        marco_config = tk.Frame(self, bg="#f4f4f4")
        marco_config.pack(fill="x")

        # Botón izquierdo (Editar)
        tk.Button(marco_config, text="Editar settup", bg="#607D8B", fg="white", 
                  command=self.abrir_config, relief="flat").pack(side="left", expand=True, fill="x", padx=(0, 5))

        # Botón derecho (Aplicar)
        self.btn_aplicar = tk.Button(marco_config, text="Aplicar", bg="#FF9800", fg="white", 
                  command=self.aplicar_config, relief="flat")
        self.btn_aplicar.pack(side="right", expand=True, fill="x", padx=(5, 0))

        threading.Thread(target=self.monitorear, daemon=True).start()

    def crear_fila(self, nombre, comando):
        marco = tk.Frame(self, bg="#f4f4f4")
        marco.pack(fill="x", pady=5)
        tk.Label(marco, text=nombre, bg="#f4f4f4").pack(side="left")
        btn = tk.Button(marco, text="Iniciar", width=10, bg="#4CAF50", fg="white", relief="flat", command=comando)
        btn.pack(side="right")
        return btn

    def monitorear(self):
        while True:
            url = f"http://{self.ip_esp}/json"
            try:
                requests.get(url, timeout=2)
                self.lbl_status.config(text="ONLINE", fg="green")
            except:
                self.lbl_status.config(text="OFFLINE", fg="red")
            time.sleep(5)

    def toggle_captura(self):
        script = os.path.join(BASE_DIR, "captura.py")
        if self.proceso_logger is None or self.proceso_logger.poll() is not None:
            try:
                self.proceso_logger = subprocess.Popen([sys.executable, script], cwd=BASE_DIR)
                self.btn_captura.config(text="Detener", bg="#F44336")
            except Exception as e:
                print(f"Error: {e}")
        else:
            self.proceso_logger.terminate()
            self.btn_captura.config(text="Iniciar", bg="#4CAF50")

    def toggle_web(self):
        script = os.path.join(BASE_DIR, "dashboard.py")
        if self.proceso_dashboard is None or self.proceso_dashboard.poll() is not None:
            try:
                self.proceso_dashboard = subprocess.Popen([sys.executable, "-m", "streamlit", "run", script], cwd=BASE_DIR)
                self.btn_web.config(text="Detener", bg="#F44336")
            except Exception as e:
                print(f"Error: {e}")
        else:
            self.proceso_dashboard.terminate()
            self.btn_web.config(text="Iniciar", bg="#4CAF50")

    def instalar_req(self):
        req = os.path.join(BASE_DIR, "requirements.txt")
        subprocess.Popen([sys.executable, "-m", "pip", "install", "-r", req], cwd=BASE_DIR)

    def abrir_config(self):
        if os.path.exists(CONFIG_PATH):
            os.startfile(CONFIG_PATH) if sys.platform == "win32" else subprocess.run(["xdg-open", CONFIG_PATH])

    def aplicar_config(self):
        script = os.path.join(BASE_DIR, "actualizar_esp32.py")
        try:
            # 1. Ejecutamos el script para escribir en Credenciales.h
            subprocess.run([sys.executable, script], cwd=BASE_DIR, check=True)
            
            # 2. Recargamos la configuración para que el Manager use la nueva IP
            self.config = cargar_config()
            self.ip_esp = self.config.get("IP_ESP32", "127.0.0.1")
            self.lbl_ip.config(text=f"ESP32 ({self.ip_esp}):")
            
            # 3. Damos feedback visual cambiando el botón a verde un par de segundos
            self.btn_aplicar.config(text="¡Aplicado!", bg="#4CAF50")
            self.after(2000, lambda: self.btn_aplicar.config(text="Aplicar", bg="#FF9800"))
            
        except Exception as e:
            print(f"Error al aplicar: {e}")
            self.btn_aplicar.config(text="Error", bg="#F44336")
            self.after(2000, lambda: self.btn_aplicar.config(text="Aplicar", bg="#FF9800"))

if __name__ == "__main__":
    app = PanelControl()
    app.mainloop()