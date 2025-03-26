#include <WiFi.h>

const char* ssid = "test2024";
const char* password = "98989898";

void setup() {
  Serial.begin(115200);
  initWiFi();
  //Imprime la intensidad de la signal
  Serial.print("RRSI: ");
  Serial.println(WiFi.RSSI());
}

void initWiFi(){
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Conectando al WiFi...");
  while(WiFi.status() != WL_CONNECTED){
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}


void loop() {
  // put your main code here, to run repeatedly:

}
