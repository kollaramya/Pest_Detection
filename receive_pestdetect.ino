#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "realme 10";
const char* password = "12334445555";
ESP8266WebServer server(80);

const int grasshopperPin = D2;
const int mothPin = D1;
const int waspPin = D0;

void handleDisplay() {
  if (server.hasArg("pest_name")) {
    String pestName = server.arg("pest_name");
    Serial.print("Received pest name: ");
    Serial.println(pestName);

    // Turn off all LEDs
    digitalWrite(grasshopperPin, LOW);
    digitalWrite(mothPin, LOW);
    digitalWrite(waspPin, LOW);

    // Turn on the corresponding LED based on the detected pest
    if (pestName.equals("grasshoper")) {
      digitalWrite(grasshopperPin, HIGH);
    } else if (pestName.equals("moth")) {
      digitalWrite(mothPin, HIGH);
    } else if (pestName.equals("wasp")) {
      digitalWrite(waspPin, HIGH);
    } else {
      Serial.println("Unknown pest detected");
    }
  }
  server.send(200, "text/plain", "Pest information received successfully.");
}

void setup() {
  Serial.begin(115200);
  Serial.println();

  pinMode(grasshopperPin, OUTPUT);
  pinMode(mothPin, OUTPUT);
  pinMode(waspPin, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  server.on("/display", handleDisplay);
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
