#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>
#include <WiFi.h>
#include <WebServer.h>

#include "credenciales.h"

#define ANCHO_PANTALLA 128
#define ALTO_PANTALLA 64
Adafruit_SSD1306 display(ANCHO_PANTALLA, ALTO_PANTALLA, &Wire, -1);

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

WebServer server(80);

const int pinHumedadSuelo = 32; 
const int pinLluvia = 33;       

const int SUELO_SECO = 4095;   
const int SUELO_MOJADO = 1500;  
const int LLUVIA_SECO = 4095;   
const int LLUVIA_MOJADO = 1200; 

float temperatura = 0, humedadAmb = 0;
int porcSuelo = 0, porcLluvia = 0;
unsigned long tiempoAnterior = 0;
const long intervalo = 2000; 

void handleRoot() {
  String html = "<html><head><meta charset='UTF-8'><meta http-equiv='refresh' content='2'>";
  html += "<style>body{font-family:Arial; text-align:center; background:#f4f4f4;} .card{background:white; padding:20px; border-radius:15px; display:inline-block; margin:10px; box-shadow:0 4px 8px rgba(0,0,0,0.1);}</style></head>";
  html += "<body><h1>🌱 Mi Estación Agrícola IoT</h1>";
  html += "<div class='card'><h2>Termómetro</h2><p style='font-size:30px;'>" + String(temperatura) + " °C</p></div>";
  html += "<div class='card'><h2>Humedad Suelo</h2><p style='font-size:30px; color:brown;'>" + String(porcSuelo) + " %</p></div>";
  html += "<div class='card'><h2>Lluvia</h2><p style='font-size:30px; color:blue;'>" + String(porcLluvia) + " %</p></div>";
  html += "<p>Para Data Science usa: <a href='/json'>/json</a></p>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

void handleJSON() {
  String json = "{";
  json += "\"temperatura\":" + String(temperatura) + ",";
  json += "\"humedad_amb\":" + String(humedadAmb) + ",";
  json += "\"suelo\":" + String(porcSuelo) + ",";
  json += "\"lluvia\":" + String(porcLluvia);
  json += "}";
  server.send(200, "application/json", json);
}

void setup() {
  Serial.begin(115200);
  dht.begin();

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("Error en pantalla OLED"));
    for(;;);
  }
  
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 10);
  display.println("Conectando Wi-Fi...");
  display.display();

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n¡Conectado!");
  
  server.on("/", handleRoot);
  server.on("/json", handleJSON);
  server.begin();
}

void loop() {
  server.handleClient();

  unsigned long tiempoActual = millis();
  if (tiempoActual - tiempoAnterior >= intervalo) {
    tiempoAnterior = tiempoActual;

    temperatura = dht.readTemperature();
    humedadAmb = dht.readHumidity();
    int sRaw = analogRead(pinHumedadSuelo);
    int lRaw = analogRead(pinLluvia);

    Serial.print("RAW Suelo: "); Serial.print(sRaw);
    Serial.print(" | RAW Lluvia: "); Serial.println(lRaw);

    porcSuelo = constrain(map(sRaw, SUELO_SECO, SUELO_MOJADO, 0, 100), 0, 100);
    porcLluvia = constrain(map(lRaw, LLUVIA_SECO, LLUVIA_MOJADO, 0, 100), 0, 100);

    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("--- ESTADO JARDIN ---");
    display.print("IP: "); display.println(WiFi.localIP()); 
    display.println("---------------------");
    display.print("Temp: "); display.print(temperatura); display.println(" C");
    display.print("Suelo: "); display.print(porcSuelo); display.println(" %");
    display.print("Lluv: "); display.print(porcLluvia); display.println(" %");

    display.setCursor(85, 35);
    display.print("/\\_/\\"); 
    display.setCursor(80, 45);
    if (random(0, 5) == 0) display.print("( ^_- )"); 
    else display.print("( ^_^ )"); 
    
    display.display();
  }
}
