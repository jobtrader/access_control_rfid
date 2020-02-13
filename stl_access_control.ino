#include <SPI.h>
#include <Ethernet.h> 
#include <Wiegand.h>
#include <String.h>

byte mac[] = {0x2C,0xF7,0xF1,0x08,0x30,0x1F};
char serverName[] = "10.28.14.60";
String host = "DESKTOP-47SAOLE";
int port = 5000;
EthernetClient client;
String type = "OUT";
int relay = 8; 

WIEGAND wg;
String gate_number = "Door1KW";


int send_request(String code) {
  // Make a HTTP request:
  Serial.println("Sending Request of Gate" + gate_number + " with id=" + code);
  if (client.connect(serverName, port)>0) {
    client.println("POST /access/rfid/" + gate_number + "?id=" + code + "&type=" + type + " HTTP/1.1");
    client.println("Host: " + host);
    client.println("Connection: close\r\n");
    delay(50);
  } else {
    Serial.println("connection failed");
  } 
  String line;
  while(client.connected()) {
      line = client.readStringUntil('\r');
  }
  int is_pass = line.toInt();
  Serial.print("Response: ");
  Serial.println(is_pass);
  client.stop();
  client.flush();
  return is_pass;
}


void setup() {
  pinMode(relay, OUTPUT);
  digitalWrite(relay, LOW);
  Serial.begin(9600);
  if(Ethernet.begin(mac) == 0) { // start ethernet using mac & IP address
    Serial.println("Failed to configure Ethernet using DHCP");  
    while(true);   // no point in carrying on, so stay in endless loop:
  }
  delay(1000); // give the Ethernet shield a second to initialize
  Serial.println("Ethernet is connected");
  wg.begin();
  Serial.print("Device IP Address: ");
  Serial.println(Ethernet.localIP());
}

void loop() {
  if (wg.available()){
    if (send_request(String(wg.getCode(),HEX))) {
      Serial.println("Opening Gate...");
      digitalWrite(relay, HIGH);
      delay(500);
      digitalWrite(relay, LOW);
      Serial.println("Closing Gate...");
    }
  }
}
